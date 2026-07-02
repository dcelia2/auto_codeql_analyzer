WITH repo_flags AS (
    SELECT
        r.id,
        strftime('%Y', r.creation_date) AS year,
        CASE
            WHEN er.repo_id IS NULL THEN 1
            ELSE 0
        END AS is_zero_issue
    FROM repos r
    LEFT JOIN error_reports er
        ON r.id = er.repo_id
    GROUP BY r.id
)

SELECT
    year,
    COUNT(*) AS total_repos,
    SUM(is_zero_issue) AS nb_repos_zero_issue,
    100.0 * SUM(is_zero_issue) / COUNT(*) AS pct_zero_issue
FROM repo_flags
GROUP BY year
ORDER BY year DESC;
