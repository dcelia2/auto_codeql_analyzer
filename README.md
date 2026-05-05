# Auto Codeql Analyzer

## Utilisation :

prérequis : 
 - un fichier json_index.json
 - avoir docker et docker compose installé
 - sqlite3 (optionnel)

configuration avant build :
 - ouvrir ```main.sh```
 - modifier les valeurs de ```DL_THREADS``` et ```CQL_THREADS```
 en fonction de votre machine (recommandé 50, 5)
 - ajouter votre ```GITHUB_TOKEN``` afin de bypasser la limite de 60 requetes (= 60 repos) par heure de github api.

 étapes de lancement : 
- cloner le repo
- placer le json_index.json dans ```data```
- ```docker compose build```
- ```docker compose up```

interprétation des données :
le programme fourni une base de donnée SQLITE
contenant 3 tables 
 - ```repos``` contients toutes les infos des repository
 - ```error_reports``` contient les erreurs levés
 - ```error_catalog``` contient la liste des différentes erreures levées.

