SELECT 
    year,
    COUNT(*) AS total_repos,
    SUM(CASE WHEN has_issue = 0 THEN 1 ELSE 0 END) AS nb_repos_zero_issue,
    100.0 * SUM(CASE WHEN has_issue = 0 THEN 1 ELSE 0 END) / COUNT(*) AS pct_zero_issue
FROM (
    SELECT 
        r.id,
        strftime('%Y', r.creation_date) AS year,
        CASE 
            WHEN er.repo_id IS NULL THEN 0 
            ELSE 1 
        END AS has_issue
    FROM repos r
    LEFT JOIN error_reports er
        ON r.id = er.repo_id
    GROUP BY r.id
)
GROUP BY year
ORDER BY year;
