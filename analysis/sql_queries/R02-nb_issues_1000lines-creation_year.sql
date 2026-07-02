/*      Autre version :
Calcul du nombre moyen d'erreurs par repos pour chaque année 
*/
SELECT 
    year,
    COUNT(*) AS nb_repos,
    AVG(repo_total_per_1000) AS occ_par_repo
FROM (
    SELECT 
        r.id,
        CAST(strftime('%Y', r.creation_date) AS INTEGER) AS year,
        COALESCE(SUM(er.occurrence_count), 0) * 1000.0 / r.nb_lines AS repo_total_per_1000
    FROM repos r
    LEFT JOIN error_reports er 
        ON r.id = er.repo_id
    WHERE r.nb_lines > 0
    GROUP BY r.id, r.creation_date, r.nb_lines
) sub
GROUP BY year
ORDER BY year ASC;
