# Auto Codeql Analyzer

## Usage:

Prerequisites: 
 - A JSON file containing a list of GitHub repositories(src/json_index.json).
 - Docker must be installed
 - SQLite3 (optional)

Steps to run: 
- Clone the repository
- ```./start.sh```

Configuration:
- In the interface window, enter a valid GitHub token with ‘repos’ permissions
- Enter the requested information
All configuration settings will be stored in the ```config.json``` file generated after the application is launched for the first time.

Notes:
- The ```generated``` folder contains execution artefacts and can be deleted once the full analysis is complete.
- CodeQL will download several GB of Maven dependencies; these are stored in your ```~/.m2``` directory so that they do not need to be re-downloaded between runs. 

Interpreting the data:
The programme provides a SQLite database (output.db)
containing four tables:
 - ```repos``` contains all repository information
 - ```error_reports``` contains the types of issues raised, their occurrences per repository, and the IDs of those repositories
 - ```error_catalog``` contains a list of the various issues raised in at least one repository (positive identifiers) or never encountered (negative identifiers).
 - ```repo_categories``` contains the repository identifiers and their categories (if they have more than one: one row per category)
