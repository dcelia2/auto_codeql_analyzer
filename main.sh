#!/usr/bin/bash

GITHUB_TOKEN=${GITHUB_TOKEN:-""}

DL_THREADS=100
CQL_THREADS=10

NB_REPOS_BY_PASS=100

JSON_FILENAME="data/json_index.json"

set -euo pipefail

# PARTIE 1

./src/initialization.sh $JSON_FILENAME $NB_REPOS_BY_PASS

for file in json/*.json; do 

  nb_repos=$(jq 'length' $file)

  echo "$nb_repos repos détéctés"

  # PARTIE 2
  ./src/create_sqlite_bd.sh $nb_repos

  # PARTIE 3
  ./src/get_repos.sh $file $nb_repos $DL_THREADS $GITHUB_TOKEN

  # PARTIE 4
  ./src/launch_codeql_analyze.sh $nb_repos $CQL_THREADS

  # PARTIE 5
  ./src/fill_db_with_json_infos.sh $nb_repos

  # PARTIE 6
  ./src/fill_db_with_csv_infos.sh $nb_repos

  # PARTIE 7
  ./src/fill_db_with_nb_lines.sh

done
