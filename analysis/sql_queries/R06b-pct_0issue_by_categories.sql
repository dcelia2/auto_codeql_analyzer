
SELECT
    rc.category,
    COUNT(DISTINCT rc.repo_id) AS total_repos,
    COUNT(
        DISTINCT CASE
            WHEN er.repo_id IS NULL THEN rc.repo_id
        END
    ) AS zero_issue_repos,
    100.0 * COUNT(
        DISTINCT CASE
            WHEN er.repo_id IS NULL THEN rc.repo_id
        END
    ) / COUNT(DISTINCT rc.repo_id) AS percentage_zero_issue
FROM repo_categories rc
LEFT JOIN (
    SELECT DISTINCT repo_id
    FROM error_reports
) er
    ON rc.repo_id = er.repo_id

GROUP BY rc.category
HAVING COUNT(DISTINCT rc.repo_id) >= 10
ORDER BY percentage_zero_issue DESC;

