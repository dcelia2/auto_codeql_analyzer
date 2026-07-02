SELECT
    strftime('%Y', r.last_commit_date) AS last_commit,
    COUNT(*) AS total_occurrences,
    SUM(CASE WHEN er.repo_id IS NULL THEN 1 ELSE 0 END) AS repos_0_issue,
    SUM(CASE WHEN er.repo_id IS NOT NULL THEN 1 ELSE 0 END) AS repos_1_plus_issue
FROM repos r
LEFT JOIN (
    SELECT DISTINCT repo_id
    FROM error_reports
) er
    ON r.id = er.repo_id
GROUP BY last_commit
ORDER BY last_commit ASC
