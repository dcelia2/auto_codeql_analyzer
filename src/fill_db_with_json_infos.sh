#!/bin/bash

echo ""
echo -e "\033[36m[- PARTIE 5 PARSING JSON -]\033[0m"
echo ""

# Configuration
DB_NAME=$3
JSON_FILE=$2
counter=1

# Vérification de l'existence des fichiers
if [ ! -f "$DB_NAME" ]; then echo "Erreur : Base de données introuvable."; exit 1; fi
if [ ! -f "$JSON_FILE" ]; then echo "Erreur : Fichier JSON introuvable."; exit 1; fi

# 2. Extraction et insertion des données
jq -c '.[]' "$JSON_FILE" | while read -r item; do

    start=$SECONDS

    # Extraction des valeurs
    id=$(echo "$item" | jq -r '.id')
    stars=$(echo "$item" | jq -r '.stars_by_github // 0')
    source_code=$(echo "$item" | jq -r '.source_code // ""')
    last_commit_date=$(echo "$item" | jq -r '.last_activity_at_by_github // ""')

    # Transformation de la liste des catégories ["A", "B"] en chaîne "A, B"
    categories=$(echo "$item" | jq -r '.categories | join(", ") // ""')
    created_at=$(echo "$item" | jq -r '.created_at_by_github // ""')

    # Mise à jour de la table repos
    sqlite3 "$DB_NAME" <<EOF
      UPDATE repos 
      SET stars = $stars, 
          categories = '$categories', 
          url = '$source_code',
          creation_date = '$created_at',
	  last_commit_date='$last_commit_date'
      WHERE id = '$id';

      INSERT OR IGNORE INTO repos (id, stars, categories, url, creation_date, last_commit_date) 
      VALUES ('$id', $stars, '$categories', '$source_code', '$created_at', '$last_commit_date');
EOF
	# Insertion dans repo_categories
      echo "$item" | jq -r '.categories[]?' | while read -r cat; do
    	safe_cat=$(echo "$cat" | sed "s/'/''/g")

    sqlite3 "$DB_NAME" <<EOF
	INSERT OR IGNORE INTO repo_categories (repo_id, category)
	VALUES ('$id', '$safe_cat');
EOF

done
    printf "Mis à jour : %-40s progression: %d/%d  [%ds]\n" "$id" "$counter" "$1" "$((SECONDS - start))"
    ((counter++))
done

echo "Importation JSON terminée."

