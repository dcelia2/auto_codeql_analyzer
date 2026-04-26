#!/usr/bin/bash

process_repo() {
    local repo_dir=$1
    local id
    id=$(basename "$repo_dir")

    echo "[START] $id"

    # Création de la base
    codeql database create "dbs/$id" \
        --language=java \
        --build-mode=none \
        --source-root="$repo_dir" \
        --overwrite \
        2>&1 | sed "s/^/[$id] /"

    # Analyse avec le pack custom
    codeql database analyze "dbs/$id" \
        green-code-initiative/java-queries@1.0.12 \
        --format=csv \
        --output="results/$id.csv" \
        --download \
        2>&1 | sed "s/^/[$id] /"

    # Suppression de la base
    rm -rf "dbs/$id"

    echo "[DONE] $id"
}

for repo_dir in repos/*/; 
do 
    process_repo "$repo_dir" 
done
