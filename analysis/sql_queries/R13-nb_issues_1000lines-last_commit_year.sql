SELECT
    year,
    AVG(repo_total) AS avg_occurrences_per_repo,
    COUNT(DISTINCT r.id) AS nb_repos
FROM (
    SELECT 
        r.id,
        CAST(strftime('%Y', r.creation_date) AS INTEGER) AS year,
        (SUM(er.occurrence_count) * 1000.0 / r.nb_lines) AS repo_total
    FROM repos r
    JOIN error_reports er ON r.id = er.repo_id
    GROUP BY r.id, year
) sub
JOIN repos r ON r.id = sub.id
GROUP BY year
ORDER BY year;
