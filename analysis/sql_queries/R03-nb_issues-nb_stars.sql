-- Calcul de la moyenne du nombre de problèmes par repos pour chaque nb d'étoiles

/*
SELECT sub.stars AS nb_etoiles, 
       AVG(sub.total_problems) AS moy_prob_par_repo 
FROM ( 
	SELECT r.id, r.stars, SUM(er.occurrence_count) AS total_problems 
	FROM repos r 
	JOIN error_reports er ON r.id = er.repo_id 
	GROUP BY r.id, r.stars 
) sub 
GROUP BY sub.stars 
ORDER BY nb_etoiles DESC;
*/

SELECT 
    sub.stars AS nb_etoiles,
    AVG(sub.errors_per_1000_lines) AS moy_prob_par_repo
FROM (
    SELECT 
        r.id,
        r.stars,
        SUM(er.occurrence_count) * 1000.0 / r.nb_lines AS errors_per_1000_lines
    FROM repos r
    JOIN error_reports er
        ON r.id = er.repo_id
    WHERE r.nb_lines > 0
    GROUP BY r.id, r.stars, r.nb_lines
) sub
GROUP BY sub.stars
ORDER BY sub.stars DESC;
