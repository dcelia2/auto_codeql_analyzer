#!/usr/bin/bash
start=$SECONDS

process_repo() {
    local repo_dir=$1
    local id
    id=$(basename "$repo_dir")


    # Création de la base
    codeql database create "dbs/$id" \
        --language=java \
        --build-mode=none \
        --source-root="$repo_dir" \
        --overwrite \
        2>&1 | >> logs

    # Analyse avec le pack custom
    codeql database analyze "dbs/$id" \
        green-code-initiative/java-queries@1.0.12 \
        --format=csv \
        --output="results/$id.csv" \
        --download \
        2>&1 | >> logs

    # Suppression de la base
    rm -rf "dbs/$id"

}

counter=1

echo "[- PARTIE 3 ANALYSE -]"

echo "début de l'analyse..."

for repo_dir in repos/*/; 
do 
    process_repo "$repo_dir" 

    printf "Repo analysé : %-40s progression: %d/%d  [%ds]\n" "$(basename $repo_dir)" "$counter" "$1" "$((SECONDS - start))"
    ((counter++))
done
