SELECT
    ec.error_name,
    COUNT(DISTINCT er.repo_id) AS nb_repos
FROM error_catalog ec
LEFT JOIN error_reports er
    ON er.error_id = ec.error_id
GROUP BY ec.error_name
ORDER BY nb_repos DESC;
