#!/bin/bash

set -euo pipefail

start=$SECONDS
INPUT="$1"
N="$2"

BUFFER=$(mktemp /tmp/buffer_XXXX.json)


if [ ! -f "$INPUT" ]; then
  echo "Erreur : fichier '$INPUT' introuvable."
  exit 1
fi

echo ""
echo -e "\033[36m[- PARTIE 1 INITIALISATION -]\033[0m"
echo ""

# Création de l'arborescence
mkdir -p repos results dbs data 2>&1 | >>  logs

# Séléction des repos appropriés
jq '[.[] | select(.language_by_github == "Java")]' "$INPUT" > "$BUFFER"

TYPE=$(jq -r 'type' "$BUFFER")
if [ "$TYPE" != "array" ]; then
  echo "Erreur : le fichier JSON doit contenir un tableau (type détecté : $TYPE)."
  exit 1
fi

TOTAL=$(jq 'length' "$BUFFER")
echo "Fichier   : $INPUT"
echo "Éléments  : $TOTAL"
echo "Par chunk : $N"

if [ "$TOTAL" -eq 0 ]; then
  echo "Le tableau est vide, rien à faire."
  exit 0
fi

# --- Création du dossier de sortie ---
mkdir -p json

# --- Découpage ---
PART=1
OFFSET=0

while [ "$OFFSET" -lt "$TOTAL" ]; do
  OUTFILE="json/part_$(printf '%04d' "$PART").json"
  jq --argjson offset "$OFFSET" --argjson n "$N" '.[$offset : $offset + $n]' "$BUFFER" > "$OUTFILE"
  COUNT=$(jq 'length' "$OUTFILE")
  echo "  -> $OUTFILE  ($COUNT élément(s))"
  PART=$((PART + 1))
  OFFSET=$((OFFSET + N))
done

echo "Terminé : $((PART - 1)) fichier(s) créé(s) dans ./json/"
