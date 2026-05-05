FROM ubuntu:24.04
 
ARG CODEQL_VERSION=2.25.2
 
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    unzip \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*
 
RUN curl -fsSL \
    "https://github.com/github/codeql-action/releases/download/codeql-bundle-v${CODEQL_VERSION}/codeql-bundle-linux64.tar.gz" \
    -o /tmp/codeql.tar.gz \
    && tar -xzf /tmp/codeql.tar.gz -C /usr/local \
    && rm /tmp/codeql.tar.gz
 
ENV PATH="/usr/local/codeql:${PATH}"

COPY src/* /workspace/src/
COPY main.sh /workspace/
 
WORKDIR /workspace
 
CMD ["./main.sh"]
#CMD ["/bin/bash"]
