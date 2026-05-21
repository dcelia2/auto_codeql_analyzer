#!/bin/bash

TOTAL=$1
THREADS=$2
counter=1

process_repo() {
    local repo_dir=$1
    local id
    id=$(basename "$repo_dir")

    start=$SECONDS

    # Création de la base
    codeql database create "generated/dbs/$id" \
        --language=java \
        --build-mode=none \
        --source-root="$repo_dir" \
        --overwrite \
        2>&1 | >> logs

    if [ $? -ne 0 ]; then
        echo "ERREUR création DB : $id" 
        return 1  
    fi

    # Analyse avec le pack custom
    codeql database analyze "generated/dbs/$id" \
        green-code-initiative/java-queries@1.0.12 \
        --format=csv \
        --output="generated/results/$id.csv" \
        2>&1 | >> logs

    # Suppression de la base
    rm -rf "dbs/$id"
    
    printf "Repo analysé : %-40s progression: %d/%d  [%ds]\n" "$id" "$2" "$3" "$((SECONDS - start))"


}

echo ""
echo -e "\033[36m[- PARTIE 4 ANALYSE -]\033[0m"
echo ""

echo "début de l'analyse..."

for repo_dir in generated/repos/*/; 
do 
  while [ "$(jobs -rp | wc -l)" -ge "$THREADS" ]; 
  do
    sleep 0.5
  done
    process_repo "$repo_dir" "$counter" "$TOTAL" &
    ((counter++))

done

wait
