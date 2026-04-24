#!/usr/bin/bash

extract_java_repos() {
    jq '[.[] | select(.language_by_github == "Java")]' json_index.json > java_repo.json
}

download_java_files() {
    local repo=$1
    local output_dir=$2
    
    curl -s "https://api.github.com/repos/$repo/git/trees/HEAD?recursive=1" \
        | jq -r '.tree[] | select(.path | endswith(".java")) | .path' \
        | while read -r filepath; do
            mkdir -p "$output_dir/$(dirname "$filepath")"
            curl -s "https://raw.githubusercontent.com/$repo/HEAD/$filepath" \
                 -o "$output_dir/$filepath"
            echo "$filepath"
        done
}

get_repos() {
    local json_file=$1
    
    while IFS= read -r line; do
        id=$(echo "$line" | jq -r '.id')
        url=$(echo "$line" | jq -r '.source_code' | sed 's|https://github.com/||')
        
        echo "ID: $id | Repo: $url"
        mkdir -p repos/$id
        download_java_files "$url" "repos/$id"
        
    done < <(jq -c '.[]' "$json_file")
}

# Utilisation
extract_java_repos
get_repos "java_repo.json"
