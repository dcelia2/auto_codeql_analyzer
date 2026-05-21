#!/usr/bin/bash
set -euo pipefail

# ─────────────────────────────────────────
#  COULEURS & STYLES
# ─────────────────────────────────────────
BOLD="--bold"
GREEN="--foreground 82"
RED="--foreground 196"
YELLOW="--foreground 220"
CYAN="--foreground 51"
DIM="--foreground 240"


clear

header() {
    clear
    gum style \
        --border double \
        --border-foreground 51 \
        --padding "1 4" \
        --margin "1 0" \
        --bold \
        --foreground 51 \
        "⬡  CodeQL Pipeline"
    echo ""
}

step_banner() {
    local num="$1"
    local label="$2"
    echo ""
    gum style \
        --border normal \
        --border-foreground 220 \
        --padding "0 2" \
        $BOLD \
        --foreground 220 \
        "ÉTAPE $num / 7 — $label"
    echo ""
}

ok()   { gum style $GREEN $BOLD "  ✓ $1"; }
err()  { gum style $RED   $BOLD "  ✗ $1"; }
info() { gum style $CYAN        "  → $1"; }
dim()  { gum style $DIM         "    $1"; }

run_step() {
    local title="$1"
    shift
    gum spin --spinner dot --title " $title..." -- "$@"
    ok "$title"
}

header

CONFIG_FILE="./config.json"

# ─────────────────────────────────────────
#  VALEURS PAR DÉFAUT
# ─────────────────────────────────────────
DEFAULT_DL_THREADS=100
DEFAULT_CQL_THREADS=10
DEFAULT_NB_REPOS_BY_PASS=100
DEFAULT_JSON_FILENAME="data/json_index.json"
DEFAULT_QLPACK_VERSION="1.0.12"

# ─────────────────────────────────────────
#  CHARGEMENT CONFIG EXISTANTE
# ─────────────────────────────────────────
if [[ -f "$CONFIG_FILE" ]]; then
    GITHUB_TOKEN=$(jq -r '.github_token      // empty' "$CONFIG_FILE")
    DL_THREADS=$(jq -r   '.dl_threads        // empty' "$CONFIG_FILE")
    CQL_THREADS=$(jq -r  '.cql_threads       // empty' "$CONFIG_FILE")
    NB_REPOS_BY_PASS=$(jq -r '.nb_repos_by_pass // empty' "$CONFIG_FILE")
    JSON_FILENAME=$(jq -r '.json_filename     // empty' "$CONFIG_FILE")
    QLPACK_VERSION=$(jq -r '.qlpack_version   // empty' "$CONFIG_FILE")
fi

# Fallback sur les défauts si champ vide
DL_THREADS=${DL_THREADS:-$DEFAULT_DL_THREADS}
CQL_THREADS=${CQL_THREADS:-$DEFAULT_CQL_THREADS}
NB_REPOS_BY_PASS=${NB_REPOS_BY_PASS:-$DEFAULT_NB_REPOS_BY_PASS}
JSON_FILENAME=${JSON_FILENAME:-$DEFAULT_JSON_FILENAME}
QLPACK_VERSION=${QLPACK_VERSION:-$DEFAULT_QLPACK_VERSION}

# ─────────────────────────────────────────
#  SAUVEGARDE CONFIG 
# ─────────────────────────────────────────
save_config() {
    jq -n \
        --arg token    "$GITHUB_TOKEN" \
        --arg dl       "$DL_THREADS" \
        --arg cql      "$CQL_THREADS" \
        --arg repos    "$NB_REPOS_BY_PASS" \
        --arg json     "$JSON_FILENAME" \
        --arg qlpack   "$QLPACK_VERSION" \
        '{
            github_token:    $token,
            dl_threads:      $dl,
            cql_threads:     $cql,
            nb_repos_by_pass: $repos,
            json_filename:   $json,
            qlpack_version:  $qlpack
        }' > "$CONFIG_FILE"
    chmod 600 "$CONFIG_FILE"
}

# ─────────────────────────────────────────
#  GITHUB TOKEN
# ─────────────────────────────────────────
gum style $BOLD $CYAN "Configuration de la pipeline"
echo ""

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    info "GitHub Token non défini"
    GITHUB_TOKEN=$(gum input \
        --placeholder "ghp_xxxxxxxxxxxxxxxxxxxx" \
        --prompt "  Token GitHub › ")
    if [[ -z "$GITHUB_TOKEN" ]]; then
        err "Token GitHub requis. Abandon."
        exit 1
    fi
    save_config
    ok "Token sauvegardé"
else
    ok "Token GitHub chargé depuis $CONFIG_FILE"
fi

echo ""

# ─────────────────────────────────────────
#  PARAMÈTRES AVANCÉS
# ─────────────────────────────────────────
if gum confirm "  Modifier les paramètres avancés ?" --default=false; then
    echo ""
    gum style $DIM "  (Entrée pour garder la valeur actuelle)"
    echo ""

    QLPACK_VERSION=$(gum input \
        --placeholder "$QLPACK_VERSION" --value "$QLPACK_VERSION" \
        --prompt "  Version du pack de requêtes › ")

    DL_THREADS=$(gum input \
        --placeholder "$DL_THREADS" --value "$DL_THREADS" \
        --prompt "  Threads de téléchargement › ")

    CQL_THREADS=$(gum input \
        --placeholder "$CQL_THREADS" --value "$CQL_THREADS" \
        --prompt "  Threads CodeQL › ")

    NB_REPOS_BY_PASS=$(gum input \
        --placeholder "$NB_REPOS_BY_PASS" --value "$NB_REPOS_BY_PASS" \
        --prompt "  Repos par passe › ")

    JSON_FILENAME=$(gum input \
        --placeholder "$JSON_FILENAME" --value "$JSON_FILENAME" \
        --prompt "  Fichier JSON index › ")

    save_config
    ok "Configuration sauvegardée dans $CONFIG_FILE"
fi
───────────────────────────────────────

# ─────────────────────────────────────────
#  RÉCAPITULATIF
# ─────────────────────────────────────────
header

gum style $BOLD "  Récapitulatif"
echo ""
dim "Token GitHub    : ${GITHUB_TOKEN:0:8}••••••••••••"
dim "DL Threads      : $DL_THREADS"
dim "CodeQL Threads  : $CQL_THREADS"
dim "Repos / passe   : $NB_REPOS_BY_PASS"
dim "JSON index      : $JSON_FILENAME"
echo ""

gum confirm "  Lancer la pipeline ?" || { info "Annulé."; exit 0; }

# ─────────────────────────────────────────
#  EXÉCUTION
# ─────────────────────────────────────────
header

# ── ÉTAPE 1 ──────────────────────────────
step_banner 1 "Initialisation"
run_step "Initialisation" \
   ./src/initialization.sh "data/json_index.json" 100 > data/logs.txt

# ── ÉTAPE 2 ──────────────────────────────
step_banner 2 "Création de la base SQLite"

# Récupère le nombre de repos depuis le premier fichier JSON
FIRST_JSON=$(ls json/*.json 2>/dev/null | head -1 || true)
if [[ -z "$FIRST_JSON" ]]; then
    err "Aucun fichier JSON trouvé dans json/"
    exit 1
fi
NB_REPOS=$(jq 'length' "$FIRST_JSON")

run_step "Création BDD SQLite" \
    ./src/create_sqlite_bd.sh "$NB_REPOS"

# ── BOUCLE SUR LES FICHIERS JSON ─────────
TOTAL_FILES=$(ls json/*.json | wc -l)
CURRENT=0

for file in json/*.json; do
    CURRENT=$((CURRENT + 1))
    NB_REPOS=$(jq 'length' "$file")

    echo ""
    gum style $DIM "  Fichier $CURRENT/$TOTAL_FILES : $file  ($NB_REPOS repos)"
    echo ""

    # ── ÉTAPE 3 ────────────────────────────
    step_banner 3 "Téléchargement des repos"
    run_step "Téléchargement ($NB_REPOS repos, $DL_THREADS threads)" \
        ./src/get_repos.sh "$file" "$NB_REPOS" "$DL_THREADS" "$GITHUB_TOKEN"

    # ── ÉTAPE 4 ────────────────────────────
    step_banner 4 "Analyse CodeQL"
    run_step "Analyse CodeQL ($CQL_THREADS threads)" \
        ./src/launch_codeql_analyze.sh "$NB_REPOS" "$CQL_THREADS"

    # ── ÉTAPE 5 ────────────────────────────
    step_banner 5 "Remplissage BDD — infos JSON"
    run_step "Import JSON → BDD" \
        ./src/fill_db_with_json_infos.sh "$NB_REPOS" "$file"

    # ── ÉTAPE 6 ────────────────────────────
    step_banner 6 "Remplissage BDD — infos CSV"
    run_step "Import CSV → BDD" \
        ./src/fill_db_with_csv_infos.sh "$NB_REPOS"

    # ── ÉTAPE 7 ────────────────────────────
    step_banner 7 "Comptage des lignes"
    run_step "Calcul nb lignes de code" \
        ./src/fill_db_with_nb_lines.sh
done

# ─────────────────────────────────────────
#  FIN
# ─────────────────────────────────────────
echo ""
gum style \
    --border double \
    --border-foreground 82 \
    --padding "1 4" \
    --margin "1 0" \
    $BOLD \
    --foreground 82 \
    "✓  Pipeline terminée avec succès"
echo ""
