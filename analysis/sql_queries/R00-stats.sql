.print ====================================
.print       	Statistiques générales
.print ====================================
.print


-- Nombre de repos analysés
.print Nombre de repos analysés :
	  SELECT COUNT(*) FROM repos;
.print ____________________________________

-- Nombres de repos présents dans le fichier .json initial
-- Pour l'obtenir :
	-- Aller dans le dossier analyse
	-- Taper dans la console : jq 'length' android-apps.json
	-- Le résultat qui s'affiche est le nombre de repo

-- Periode création des repos analysés
.print Période de création des repos analysés :
	  SELECT 
	      MIN(creation_date) || ' - ' || MAX(creation_date)
	  FROM repos;
.print ____________________________________


-- Periode de dernieres mises à jour des repos analysés
.print Période de dernières mises à jour des repos analysés :
	  SELECT
	     MIN(last_commit_date) || ' - ' || MAX(last_commit_date)
	  FROM repos;
.print ____________________________________

-- Durée de vie moyenne d'un projet 
.print Durée de vie moyenne d'un projet (en année):
	  SELECT AVG((julianday(last_commit_date) - julianday(creation_date)) / 365.25)
	  FROM repos
	  WHERE creation_date IS NOT NULL
	    AND last_commit_date IS NOT NULL;
.print ____________________________________


-- Nombre de types d'issue differents
.print Nombre de types d'issue différents :
	  SELECT COUNT(*) FROM error_catalog;
.print ____________________________________

-- Nombre de catégories différentes
.print Nombre de catégories différentes :
	  SELECT COUNT(DISTINCT category) FROM repo_categories;
.print ____________________________________

-- Nombre total d'issues trouvées
.print Nombre total d'issues trouvées :
	SELECT SUM(occurrence_count) AS total_errors
	FROM error_reports;
.print ____________________________________

-- Nombre moyen de lignes des repos
.print Nombre moyen de lignes des repos analysés :
	SELECT AVG(nb_lines)
	FROM repos
	WHERE nb_lines > 0;
.print ____________________________________

-- Repo avec 0 issue :

	-- Nombre repo avec 0 issue
.print Nombre de repo avec 0 issue :
  	SELECT COUNT(*) FROM repos
	  WHERE id NOT IN (
	      SELECT DISTINCT repo_id
	      FROM error_reports
	  );
.print ____________________________________


	-- Nombre moyen de lignes
.print Nombre moyen de lignes des repos avec 0 issue :
	  SELECT AVG(nb_lines) FROM repos
	  WHERE id NOT IN (
 	      SELECT DISTINCT repo_id FROM error_reports
	);
.print _____________________________________

	-- Nombre moyen d'étoiles
.print Nombre moyen d'étoiles des repos avec 0 issue :
	  SELECT AVG(stars) FROM repos
	  WHERE id NOT IN (
	      SELECT DISTINCT repo_id FROM error_reports
	  );
.print _____________________________________

	-- Date moyenne de dernière mise à jour :
.print Jour moyen de dernière mise à jour des repos avec 0 issue :
	SELECT DATE(AVG(julianday(last_commit_date)))  FROM repos
	WHERE id NOT IN (
	    SELECT DISTINCT repo_id
	    FROM error_reports
	);
.print _____________________________________

-- Repo avec au moins 1 issue :

	-- Nombre moyen de lignes :
.print Nombre moyen de lignes des repos avec 1 issue ou plus :
	SELECT AVG(nb_lines)  FROM repos
	WHERE id IN (
	    SELECT DISTINCT repo_id
	    FROM error_reports
	);
.print ____________________________________

	-- Nombre moyen d'étoiles
.print Nombre moyen d'étoiles des repos avec 1 issue ou plus :
	SELECT AVG(stars)  FROM repos
	WHERE id IN (
	    SELECT DISTINCT repo_id
	    FROM error_reports
	);
.print ____________________________________

	-- Date moyenne de dernière mise à jour
.print Jour moyen de dernière mise à jour des repos ayant au moins 1 issue:
	SELECT DATE(AVG(julianday(last_commit_date)))  FROM repos
	WHERE id IN (
	    SELECT DISTINCT repo_id
	    FROM error_reports
	);
.print ____________________________________


-- "Missing ..." issues
.print Nombre de repos ayant une "Missing ..." issue
	SELECT COUNT (DISTINCT er.repo_id)
	FROM error_reports er
	JOIN error_catalog ec
	    ON er.error_id = ec.error_id
	WHERE ec.error_name LIKE 'Missing%';
.print ____________________________________


.print Nombre total d'issues de types "Missing" trouvées
	SELECT SUM(er.occurrence_count)
	FROM error_reports er
	JOIN error_catalog ec
	    ON er.error_id = ec.error_id
	WHERE ec.error_name LIKE 'Missing%';
.print ____________________________________

	-- Nombre moyen de lignes
.print Nombre moyen de lignes des repos ayant au moins une issue "Missing ..."
	SELECT AVG(nb_lines)
	FROM repos
	WHERE id IN (
	    SELECT DISTINCT er.repo_id
	    FROM error_reports er
	    JOIN error_catalog ec
	        ON er.error_id = ec.error_id
	    WHERE ec.error_name LIKE 'Missing%'
	);
.print ____________________________________

.print Nombre moyen de lignes des repos ayant aucune issue "Missing ..."
	SELECT AVG(nb_lines)
	FROM repos
	WHERE id NOT IN (
	    SELECT DISTINCT er.repo_id
	    FROM error_reports er
	    JOIN error_catalog ec
	        ON er.error_id = ec.error_id
	    WHERE ec.error_name LIKE 'Missing%'
	);
.print ____________________________________
.print
.print

.print =========================================
.print Etude des 2 principales issues :
.print        Missing power savemode awareness
.print        Missing battery and charging state monitoring
.print =========================================
.print
.print
.print Nombre de repos qui ont au moins une des 2 :
	SELECT COUNT(DISTINCT er.repo_id)
	FROM error_reports er
	JOIN error_catalog ec
	      ON er.error_id = ec.error_id
	WHERE ec.error_name IN (
	     'Missing power save mode awareness',
	     'Missing battery and charging state monitoring'
	);
.print ____________________________________

.print Nombre total de ces issues :
	SELECT SUM(er.occurrence_count)
	FROM error_reports er
	JOIN error_catalog ec
	     ON er.error_id = ec.error_id
	WHERE ec.error_name IN (
	      'Missing power save mode awareness',
	      'Missing battery and charging state monitoring'
	);
.print ____________________________________

.print Nombre moyen de lignes de ces repos :
	SELECT AVG(nb_lines)
	FROM repos
	WHERE id IN (
	      SELECT DISTINCT er.repo_id
	      FROM error_reports er
	      JOIN error_catalog ec
	        ON er.error_id = ec.error_id
	      WHERE ec.error_name IN (
	            'Missing power save mode awareness',
	            'Missing battery and charging state monitoring'
	      )
	);
.print _______________________________
.print
.print
.print
