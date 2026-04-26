#!/bin/bash

# Configuration
DB_NAME="./data/sqlite.db"
JSON_FILE="./java_repo.json"

# Vérification de l'existence des fichiers
if [ ! -f "$DB_NAME" ]; then echo "Erreur : Base de données introuvable."; exit 1; fi
if [ ! -f "$JSON_FILE" ]; then echo "Erreur : Fichier JSON introuvable."; exit 1; fi

# 2. Extraction et insertion des données
jq -c '.[]' "$JSON_FILE" | while read -r item; do
    
    # Extraction des valeurs
    id=$(echo "$item" | jq -r '.id')
    stars=$(echo "$item" | jq -r '.stars_by_github // 0')
    source_code=$(echo "$item" | jq -r '.source_code // ""')
    
    # Transformation de la liste des catégories ["A", "B"] en chaîne "A, B"
    categories=$(echo "$item" | jq -r '.categories | join(", ") // ""')

    # Mise à jour de la table repos
    sqlite3 "$DB_NAME" <<EOF
      UPDATE repos 
      SET stars = $stars, 
          categories = '$categories', 
          url = '$source_code' 
      WHERE id = '$id';

      INSERT OR IGNORE INTO repos (id, stars, categories, url) 
      VALUES ('$id', $stars, '$categories', '$source_code');
EOF

    echo "Mis à jour : $id ($stars stars)"
done

echo "Importation JSON terminée."

