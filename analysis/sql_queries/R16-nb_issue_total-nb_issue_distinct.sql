SELECT
    ec.error_name,
    SUM(er.occurrence_count) AS total_occurrences,
    COUNT(DISTINCT er.repo_id) AS distinct_repos
FROM error_catalog ec
JOIN error_reports er
    ON ec.error_id = er.error_id
GROUP BY ec.error_id, ec.error_name
ORDER BY SUM(er.occurrence_count) DESC;
