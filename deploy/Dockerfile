# OKF MCP server image — serves the bundle over streamable-HTTP on the internal network.
FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY server/requirements.txt /app/server/requirements.txt
# Use --index-url <your internal PyPI mirror> for air-gapped builds.
RUN pip install --no-cache-dir -r /app/server/requirements.txt

COPY . /app

ENV OKF_REPO_DIR=/data/repo \
    OKF_BUNDLE=/data/repo/wiki \
    OKF_MCP_TRANSPORT=streamable-http \
    OKF_MCP_HOST=0.0.0.0 \
    OKF_MCP_PORT=8765

# Clone the bundle from the internal git server on first boot, then pull + serve.
COPY deploy/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
EXPOSE 8765
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
