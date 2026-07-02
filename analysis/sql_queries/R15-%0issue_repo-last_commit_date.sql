WITH repo_issue_count AS (
    SELECT
        r.id,
        strftime('%Y', r.last_commit_date) AS year,
        COUNT(er.error_id) AS issue_count
    FROM repos r
    LEFT JOIN error_reports er
        ON r.id = er.repo_id
    GROUP BY r.id
)

SELECT
    year,
    COUNT(*) AS total_repos,
    SUM(CASE WHEN issue_count = 0 THEN 1 ELSE 0 END) AS repos_with_0_issue,
    100.0 * SUM(CASE WHEN issue_count = 0 THEN 1 ELSE 0 END) / COUNT(*) AS percent_zero_issue
FROM repo_issue_count
GROUP BY year
ORDER BY year ASC;
