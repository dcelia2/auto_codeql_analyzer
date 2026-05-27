#!/bin/bash

GITHUB_TOKEN=$4
THREADS=$3

# Mise en place du GH token pour les requêtes
build_curl_args() {
    CURL_ARGS=(-s)
    if [[ -n "$GITHUB_TOKEN" ]]; then
        CURL_ARGS+=(-H "Authorization: token $GITHUB_TOKEN")
        echo "un token github à été trouvé"
    else 
        echo "aucun token github configuré voir README.md"
    fi
}

# Téléchargements des fichiers java d'un repo
download_java_files() {
    local repo=$1
    local output_dir=$2
    local counter=$3
    local total=$4

    mkdir -p $output_dir
    
    start=$SECONDS

    local api_response
    api_response=$(curl -s "${CURL_ARGS[@]}" "https://api.github.com/repos/$repo/git/trees/HEAD?recursive=1") 

    local error_msg
    error_msg=$(echo "$api_response" | jq -r '.message // empty')
    if [[ -n "$error_msg" ]]; then
        echo "[SKIP] $repo : $error_msg"
        rm -r $output_dir
        return 1
    fi

    local tree_check
    tree_check=$(echo "$api_response" | jq '.tree // empty')
    if [[ -z "$tree_check" ]]; then
        echo "[SKIP] $repo : arbre vide ou réponse inattendue"
        rm -r $output_dir
        return 1
    fi

    echo "$api_response" \
        | jq -r '.tree[] | select(.path | (endswith(".java") or endswith(".xml"))) | .path' \
        | while read -r filepath; do
            mkdir -p "$output_dir/$(dirname "$filepath")"
            curl -s "${CURL_ARGS[@]}" "https://raw.githubusercontent.com/$repo/HEAD/$filepath" \
                 -o "$output_dir/$filepath" >> logs 2>&1
            echo "  $filepath" >> logs
        done
    printf "Repo obtenu : %-40s progression: %d/%d  [%ds]\n" "$repo" "$counter" "$total" "$((SECONDS - start))"
}

json_file=$1
counter=1

echo ""
echo -e "\033[36m[- PARTIE 3 OBTENTION -]\033[0m"
echo ""

echo "début du téléchargement..."

build_curl_args

while IFS= read -r line; do
    id=$(echo "$line" | jq -r '.id')
    url=$(echo "$line" | jq -r '.source_code' | sed 's|https://github.com/||' | sed 's|/tree/.*||')
    while [ "$(jobs -rp | wc -l)" -ge "$THREADS" ]; do
        sleep 0.5
    done

    if [ -d "generated/repos/$id" ]; then
      echo "Dossier trouvé pour $url, téléchargement skipped"
    else
      download_java_files "$url" "generated/repos/$id" "$counter" "$2" &
      ((counter ++))
    fi

done < <(jq -c '.[]' "$json_file")

wait

echo "Tous les repos on été téléchargés"

