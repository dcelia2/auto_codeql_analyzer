#!/bin/bash

echo ""
echo -e "\033[36m[- PARTIE 6 PARSING CSV -]\033[0m" 
echo ""

# Configuration
DB_NAME="sqlite.db"
CSV_DIR="./results"
counter=1

# Vérification de l'existence des fichiers
if [ ! -f "$DB_NAME" ]; then echo "Erreur : Base de données introuvable."; exit 1; fi

# Boucle sur chaque fichier CSV
for file in "$CSV_DIR"/*.csv; do
    [ -e "$file" ] || continue

    start=$SECONDS

    # Extraction de l'ID du repo
    repo_id=$(basename "$file" .csv)

    # Insertion du repo dans la table de référence
    sqlite3 "$DB_NAME" "INSERT OR IGNORE INTO repos (id) VALUES ('$repo_id');"

    # 2. Traitement des erreurs 
    awk -F',' '{gsub(/"/, "", $1); gsub(/"/, "", $3); print $1"|"$3}' "$file" | sort | uniq -c | while read -r count data; do
        
        error_name=$(echo "$data" | cut -d'|' -f1)
        
        # Échappement des apostrophes pour SQL
        sql_safe_name=$(echo "$error_name" | sed "s/'/''/g")

        # A. Mise à jour du catalogue d'erreurs
        sqlite3 "$DB_NAME" "INSERT OR IGNORE INTO error_catalog (error_name) VALUES ('$sql_safe_name');"

        # B. Insertion ou mise à jour du rapport (table de faits)
        sqlite3 "$DB_NAME" <<EOF
INSERT INTO error_reports (repo_id, error_id, occurrence_count)
SELECT '$repo_id', error_id, $count
FROM error_catalog 
WHERE error_name = '$sql_safe_name'
ON CONFLICT(repo_id, error_id) DO UPDATE SET occurrence_count = excluded.occurrence_count;
EOF
    done

    printf "Mis à jour : %-40s progression: %d/%d  [%ds]\n" "$repo_id" "$counter" "$1" "$((SECONDS - start))"
    ((counter++))
done

echo "Traitement global terminé."
