SELECT
    strftime('%Y', r.creation_date) AS creation_year,
    COUNT(*) AS total_occurrences,
    SUM(CASE WHEN er.repo_id IS NULL THEN 1 ELSE 0 END) AS repos_0_issue,
    SUM(CASE WHEN er.repo_id IS NOT NULL THEN 1 ELSE 0 END) AS repos_1_plus_issue
FROM repos r
LEFT JOIN (
    SELECT DISTINCT repo_id
    FROM error_reports
) er
    ON r.id = er.repo_id
GROUP BY creation_year
ORDER BY creation_year ASC;
