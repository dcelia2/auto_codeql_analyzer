-- Query No. 12: Retrieves the density of green issues per 1,000 lines 
-- and the number of lines for all repositories, in order to analyse 
-- their distribution and the impact of the number of lines on the ‘cleanliness’ of the repository 

SELECT 
    r.nb_lines AS nb_lignes,
    SUM(er.occurrence_count) * 1000.0 / r.nb_lines AS issues_per_1000_lines
FROM repos r
JOIN error_reports er 
    ON r.id = er.repo_id
GROUP BY r.id, r.nb_lines
ORDER BY nb_lignes ASC;
