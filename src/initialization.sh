#!/bin/bash
start=$SECONDS

echo ""
echo -e "\033[36m[- PARTIE 1 INITIALISATION -]\033[0m"
echo ""

# Création de l'arborescence
mkdir repos results dbs data 2>&1 | >>  logs

# Séléction des repos appropriés
jq '[.[] | select(.language_by_github == "Java")]' data/json_index.json > java_repo.json

echo "programme initialisé $((SECONDS - start))"
