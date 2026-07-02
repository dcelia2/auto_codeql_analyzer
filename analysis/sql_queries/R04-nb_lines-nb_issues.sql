-- Calcule le nombre total d'erreurs du repo et son nombre de lignes

SELECT 
    r.id AS repo_id,
    r.nb_lines as nb_lignes,
    SUM(er.occurrence_count) AS total_errors
FROM repos r
JOIN error_reports er 
    ON r.id = er.repo_id
GROUP BY r.id, r.nb_lines
ORDER BY nb_lignes ASC;
