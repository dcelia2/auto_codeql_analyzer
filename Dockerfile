FROM ubuntu:24.04
 
ARG CODEQL_VERSION=2.25.2
 
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    unzip \
    git \
    sqlite3 \
    gpg \
    && rm -rf /var/lib/apt/lists/*
 
RUN curl -fsSL \
    "https://github.com/github/codeql-action/releases/download/codeql-bundle-v${CODEQL_VERSION}/codeql-bundle-linux64.tar.gz" \
    -o /tmp/codeql.tar.gz \
    && tar -xzf /tmp/codeql.tar.gz -C /usr/local \
    && rm /tmp/codeql.tar.gz

RUN \
    mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://repo.charm.sh/apt/gpg.key | gpg --dearmor -o /etc/apt/keyrings/charm.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | tee /etc/apt/sources.list.d/charm.list \
    && apt update && apt install gum

 
ENV PATH="/usr/local/codeql:${PATH}"

WORKDIR /workspace

ENTRYPOINT ./src/main.sh

