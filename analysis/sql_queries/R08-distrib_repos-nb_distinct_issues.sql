WITH repo_error_counts AS (
    SELECT 
        r.id AS repo_id,
        COUNT(DISTINCT er.error_id) AS nb_errors
    FROM repos r
    LEFT JOIN error_reports er 
        ON r.id = er.repo_id
    GROUP BY r.id
)

SELECT 
    CASE 
        WHEN nb_errors = 0 THEN '0 issue'
        WHEN nb_errors BETWEEN 1 AND 2 THEN '1-2 issues'
        WHEN nb_errors BETWEEN 3 AND 4 THEN '3-4 issues'
        WHEN nb_errors BETWEEN 5 AND 6 THEN '5-6 issues'
	WHEN nb_errors BETWEEN 7 AND 8 THEN '7-8 issues'
	WHEN nb_errors BETWEEN 9 AND 10 THEN '9-10 issues'
	WHEN nb_errors BETWEEN 11 AND 12 THEN '11-12 issues'
	WHEN nb_errors BETWEEN 13 AND 14 THEN '13-14 issues'
	WHEN nb_errors BETWEEN 16 AND 20 THEN '15-20 issues'
        ELSE '20+ issues'
    END AS categorie,
    COUNT(*) AS nb_repos
FROM repo_error_counts
GROUP BY categorie
ORDER BY 
    CASE categorie
        WHEN '0 issue' THEN 1
        WHEN '1-2 issues' THEN 2
        WHEN '3-4 issues' THEN 3
        WHEN '5-6 issues' THEN 4
	WHEN '7-8 issues' THEN 5
	WHEN '9-10 issues' THEN 6
	WHEN '11-12 issues' THEN 7
	WHEN '13-14 issues' THEN 8
	WHEN '15-20 issues' THEN 9
        ELSE 10
    END;
