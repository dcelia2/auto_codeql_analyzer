SELECT 
    ec.error_name,
    coalesce(AVG(er.occurrence_count), 0) AS avg_occurrences_per_repo
FROM error_catalog ec
LEFT JOIN error_reports er 
    ON er.error_id = ec.error_id
GROUP BY ec.error_name
ORDER BY avg_occurrences_per_repo DESC;
