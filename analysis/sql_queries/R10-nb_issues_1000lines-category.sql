SELECT
    rc.category,
    AVG(sub.errors_per_1000_lines) AS avg_errors_per_repo
FROM repo_categories rc
JOIN (
    SELECT
        r.id AS repo_id,
        SUM(er.occurrence_count) * 1000.0 / r.nb_lines AS errors_per_1000_lines
    FROM repos r
    JOIN error_reports er
        ON r.id = er.repo_id
    WHERE r.nb_lines > 0
    GROUP BY r.id, r.nb_lines
) sub
    ON rc.repo_id = sub.repo_id
GROUP BY rc.category
HAVING COUNT(DISTINCT rc.repo_id) >= 10
ORDER BY avg_errors_per_repo DESC;
