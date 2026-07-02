SELECT
    sub.category,
    AVG(sub.nb_error_types) AS avg_nb_error_types
FROM (
    SELECT
        rc.category,
        r.id,
        COUNT(DISTINCT er.error_id) AS nb_error_types
    FROM repos r
    JOIN repo_categories rc
        ON r.id = rc.repo_id
    LEFT JOIN error_reports er
        ON r.id = er.repo_id
    GROUP BY rc.category, r.id
) sub
GROUP BY sub.category
ORDER BY AVG(sub.nb_error_types) DESC;
