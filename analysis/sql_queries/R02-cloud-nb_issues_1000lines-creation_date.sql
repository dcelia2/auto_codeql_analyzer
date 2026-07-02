

/*	 Version améliorée :
Fais une moyenne du nombre d'erreurs par date de creation puis les
affiche par date décroissante
*/

SELECT 
    sub.creation_date AS date,
    AVG(sub.errors_per_1000_lines) AS avg_occurrences_per_repo
FROM (
    SELECT 
        r.id,
        r.creation_date,
        SUM(er.occurrence_count) * 1000.0 / r.nb_lines AS errors_per_1000_lines
    FROM repos r
    JOIN error_reports er
        ON r.id = er.repo_id
    WHERE r.nb_lines > 0
    GROUP BY r.id, r.creation_date, r.nb_lines
) sub
GROUP BY date
ORDER BY date DESC;
