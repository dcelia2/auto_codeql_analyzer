#!/usr/bin/bash

./src/initialization.sh
./src/get_repos.sh "java_repo.json"
./src/launch_codeql_analyze.sh
./src/create_sqlite_bd.sh
./src/fill_db_with_json_infos.sh
./src/fill_db_with_csv_infos.sh

