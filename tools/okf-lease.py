#!/usr/bin/env python3
"""okf-lease.py — advisory lease/lock manager for concurrent OKF writes.

For the "concurrent + lease/lock" write model (see docs/ENTERPRISE.md): when many
agents write at once, a short-TTL lease per concept stops two of them editing the
SAME file simultaneously. Different concepts = different files = no contention.

Single-authority by design: the MCP server is the one process that hands out leases,
so file-atomic primitives (O_CREAT|O_EXCL on one host) are sufficient. Leases are
**advisory** and **auto-expire** (a crashed agent never deadlocks a concept).

Store: OKF_LEASE_DIR (default: $TMPDIR/okf-leases). Each lease = one JSON file.

CLI:
  python3 tools/okf-lease.py acquire tables/orders --owner agentA [--ttl 300]
  python3 tools/okf-lease.py renew   tables/orders --owner agentA --token <tok> [--ttl 300]
  python3 tools/okf-lease.py release tables/orders --owner agentA --token <tok>
  python3 tools/okf-lease.py list
  python3 tools/okf-lease.py break   tables/orders        # admin force-release
"""
import argparse
import json
import os
import re
import secrets
import tempfile
import time

LEASE_DIR = os.getenv("OKF_LEASE_DIR", os.path.join(tempfile.gettempdir(), "okf-leases"))
DEFAULT_TTL = int(os.getenv("OKF_LEASE_TTL", "300"))


class Locked(RuntimeError):
    def __init__(self, holder):
        self.holder = holder
        super().__init__(f"held by {holder.get('owner')!r} until {holder.get('expires_at')}")


def _safe(concept_id):
    cid = concept_id.strip().lstrip("/")
    cid = cid[:-3] if cid.endswith(".md") else cid
    if ".." in cid.split("/") or not re.match(r"^[\w\-/]+$", cid):
        raise ValueError(f"invalid concept_id: {concept_id!r}")
    return cid


def _path(concept_id):
    return os.path.join(LEASE_DIR, _safe(concept_id).replace("/", "__") + ".lease")


def _read(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return None


def _write_atomic(path, rec):
    fd, tmp = tempfile.mkstemp(dir=LEASE_DIR)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(rec, fh)
    os.replace(tmp, path)          # atomic on POSIX


def acquire(concept_id, owner, ttl=DEFAULT_TTL):
    """Acquire a lease. Returns the lease record, or raises Locked if a live lease exists."""
    os.makedirs(LEASE_DIR, exist_ok=True)
    cid = _safe(concept_id)
    now = time.time()
    rec = {"concept": cid, "owner": owner, "token": secrets.token_hex(8),
           "acquired_at": now, "ttl": ttl, "expires_at": now + ttl}
    path = _path(cid)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)   # atomic create
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(rec, fh)
        return rec
    except FileExistsError:
        cur = _read(path)
        if cur and now < cur.get("expires_at", 0):
            raise Locked(cur)
        rec["stolen_from"] = (cur or {}).get("owner")          # expired/corrupt → steal
        _write_atomic(path, rec)
        return rec


def _verify(concept_id, owner, token):
    cur = _read(_path(concept_id))
    if not cur or cur.get("token") != token or cur.get("owner") != owner:
        raise PermissionError("not the lease holder (wrong owner/token, or lease expired/broken)")
    return cur


def renew(concept_id, owner, token, ttl=DEFAULT_TTL):
    _verify(concept_id, owner, token)
    now = time.time()
    rec = {"concept": _safe(concept_id), "owner": owner, "token": token,
           "acquired_at": now, "ttl": ttl, "expires_at": now + ttl}
    _write_atomic(_path(concept_id), rec)
    return rec


def release(concept_id, owner, token):
    _verify(concept_id, owner, token)
    os.remove(_path(concept_id))
    return {"released": _safe(concept_id)}


def break_lease(concept_id):
    p = _path(concept_id)
    existed = os.path.exists(p)
    if existed:
        os.remove(p)
    return {"broken": _safe(concept_id), "existed": existed}


def list_active():
    if not os.path.isdir(LEASE_DIR):
        return []
    now, out = time.time(), []
    for fn in os.listdir(LEASE_DIR):
        if not fn.endswith(".lease"):
            continue
        rec = _read(os.path.join(LEASE_DIR, fn))
        if rec and now < rec.get("expires_at", 0):
            out.append({"concept": rec["concept"], "owner": rec["owner"],
                        "expires_in": round(rec["expires_at"] - now, 1)})
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("acquire", "renew", "release", "break"):
        p = sub.add_parser(name)
        p.add_argument("concept")
        if name != "break":
            p.add_argument("--owner", required=(name != "acquire"), default=os.getenv("OKF_LEASE_OWNER", "agent"))
            p.add_argument("--ttl", type=int, default=DEFAULT_TTL)
        if name in ("renew", "release"):
            p.add_argument("--token", required=True)
    sub.add_parser("list")
    a = ap.parse_args()
    try:
        if a.cmd == "acquire":
            print(json.dumps(acquire(a.concept, a.owner, a.ttl)))
        elif a.cmd == "renew":
            print(json.dumps(renew(a.concept, a.owner, a.token, a.ttl)))
        elif a.cmd == "release":
            print(json.dumps(release(a.concept, a.owner, a.token)))
        elif a.cmd == "break":
            print(json.dumps(break_lease(a.concept)))
        else:
            print(json.dumps(list_active(), indent=2))
    except Locked as e:
        print(f"✗ LOCKED: {e}"); return 1
    except (PermissionError, ValueError) as e:
        print(f"✗ {e}"); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
