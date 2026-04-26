#!/usr/bin/bash
start=$SECONDS

GITHUB_TOKEN=${GITHUB_TOKEN:-""}

# Mise en place du GH token pour les requêtes
build_curl_args() {
    CURL_ARGS=(-s)
    if [[ -n "$GITHUB_TOKEN" ]]; then
        CURL_ARGS+=(-H "Authorization: token $GITHUB_TOKEN")
    fi
}

# Téléchargements des fichiers java d'un repo
download_java_files() {
    local repo=$1
    local output_dir=$2

    local api_response
    api_response=$(curl -s "${CURL_ARGS[@]}" "https://api.github.com/repos/$repo/git/trees/HEAD?recursive=1") 


    local error_msg
    error_msg=$(echo "$api_response" | jq -r '.message // empty')
    if [[ -n "$error_msg" ]]; then
        echo "  [SKIP] $repo : $error_msg"
        return 1
    fi

    local tree_check
    tree_check=$(echo "$api_response" | jq '.tree // empty')
    if [[ -z "$tree_check" ]]; then
        echo "  [SKIP] $repo : arbre vide ou réponse inattendue"
        return 1
    fi

    echo "$api_response" \
        | jq -r '.tree[] | select(.path | endswith(".java")) | .path' \
        | while read -r filepath; do
            mkdir -p "$output_dir/$(dirname "$filepath")"
            curl -s "${CURL_ARGS[@]}" "https://raw.githubusercontent.com/$repo/HEAD/$filepath" \
                 -o "$output_dir/$filepath" >> logs 2>&1
            echo "  $filepath" >> logs
        done
}

json_file=$1
counter=1

echo "[- PARTIE 2 OBTENTION -]"

echo "début du téléchargement..."

while IFS= read -r line; do
    id=$(echo "$line" | jq -r '.id')
    url=$(echo "$line" | jq -r '.source_code' | sed 's|https://github.com/||' | sed 's|/tree/.*||')


    mkdir -p "repos/$id"
    download_java_files "$url" "repos/$id"
    printf "Repo obtenu : %-40s progression: %d/%d  [%ds]\n" "$url" "$counter" "$2" "$((SECONDS - start))"
    ((counter++))

done < <(jq -c '.[]' "$json_file")

echo "Tous les repos on été téléchargés"

