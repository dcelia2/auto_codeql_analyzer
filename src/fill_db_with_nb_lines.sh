#!/bin/bash

REPOS_DIR="repos"
DB_FILE=data/sqlite.db

echo ""
echo -e "\033[36m[- PARTIE 7 COMPTAGE DES LIGNES -]\033[0m"
echo ""

# Parcours de chaque sous-dossier dans repos/
for dir in "$REPOS_DIR"/*/; do
    [ -d "$dir" ] || continue
 
    name=$(basename "$dir")
 
    # Compte toutes les lignes de tous les fichiers (récursivement)
    line_count=$(find "$dir" -type f | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
    line_count=${line_count:-0}
 
    # Insert ou met à jour l'entrée dans la base
    sqlite3 "$DB_FILE" "UPDATE repos SET nb_lines = $line_count WHERE id = '$name';"
 
    echo "$name : $line_count lignes"
done
 
echo "Résultats stockés dans '$DB_FILE'."
 
