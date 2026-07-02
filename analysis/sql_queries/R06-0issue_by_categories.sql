SELECT 
    rc.category,
    COUNT(DISTINCT rc.repo_id) AS total_repos,
    COUNT(DISTINCT CASE 
        WHEN er.repo_id IS NULL THEN rc.repo_id 
    END) AS repos_with_0_issue
FROM repo_categories rc
LEFT JOIN error_reports er
    ON rc.repo_id = er.repo_id
GROUP BY rc.category
ORDER BY repos_with_0_issue DESC;
