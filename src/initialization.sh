#!/bin/bash
start=$SECONDS

echo "[- PARTIE 1 INITIALISATION -]"

# Création de l'arborescence
mkdir repos results dbs data 2>&1 | >>  logs

# Séléction des repos appropriés
jq '[.[] | select(.language_by_github == "Java")]' json_index.json > java_repo.json

echo "programme initialisé $((SECONDS - start))"
