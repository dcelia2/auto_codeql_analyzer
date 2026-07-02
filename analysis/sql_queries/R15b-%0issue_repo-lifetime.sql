WITH repo_issue_count AS (
    SELECT
        r.id,
        (julianday(r.last_commit_date) - julianday(r.creation_date)) / 365.25 AS lifetime_years,
        COUNT(er.error_id) AS issue_count
    FROM repos r
    LEFT JOIN error_reports er
        ON r.id = er.repo_id
    GROUP BY r.id
),

classified AS (
    SELECT
        CAST(lifetime_years AS INTEGER) AS lifetime_bin,
        CASE WHEN issue_count = 0 THEN 1 ELSE 0 END AS is_zero_issue
    FROM repo_issue_count
)

SELECT
    lifetime_bin,
    COUNT(*) AS total_repos,
    SUM(is_zero_issue) AS repos_with_0_issue,
    100.0 * SUM(is_zero_issue) / COUNT(*) AS percent_zero_issue
FROM classified
GROUP BY lifetime_bin
ORDER BY lifetime_bin;
