# Auto Codeql Analyzer

## Utilisation :

prérequis : 
 - un fichier json contenant une liste de repos github.
 - avoir docker installé
 - sqlite3 (optionnel)

 étapes de lancement : 
- cloner le repo
- ```sudo ./start.sh```
 Pour relancer de zéro après avoir déjà effectué au moins une fois l'analyse :
- ```rm output.db``` 
- ```rm -rf generated/```
- ```sudo docker rm -f AutoCodeQLAnalyzer```
- ```sudo ./start.sh``` 

configuration :
- dans la fenêtre de l'interface, renseigner un github token valide avec les droits "repos"
- renseigner les informations demandées
toutes les configurations seront stockées dans le ```config.json``` généré après le premier lancement de l'application.

notes :
- le dossier ```generated``` contient les résidus d'exécution et peut être supprimé à la fin de l'analyse globale.
- codeql va télécharger beaucoup de Go de dépendances maven, elles sont stockées dans votre ```~/.m2``` afin de ne pas avoir à les re-télécharger d'une exécution sur l'autre. 

interprétation des données :
le programme fourni une base de données SQLITE (output.db)
contenant 4 tables :
 - ```repos``` contients toutes les infos des repositories
 - ```error_reports``` contient les erreurs levés pour chaque repos et leur occurrence dedans
 - ```error_catalog``` contient la liste des différentes erreurs levées ainsi que des erreurs qui n'ont jamais été trouvées (ajoutées manuellement).
 - ```repo_categories``` contient les identifiants des repos et leur(s) catégorie(s) (s'il y en a plusieurs : une ligne par catégorie)
