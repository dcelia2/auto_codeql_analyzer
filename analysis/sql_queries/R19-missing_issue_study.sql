SELECT
    r.id AS repo_id,
    r.nb_lines,
    ec.error_name AS type_error,
    COALESCE(SUM(er.occurrence_count) *1000/r.nb_lines, 1) AS occurrence
FROM repos r
LEFT JOIN error_reports er
    ON r.id = er.repo_id
LEFT JOIN error_catalog ec
    ON er.error_id = ec.error_id
    AND ec.error_name LIKE 'Missing%'
GROUP BY r.id, r.nb_lines;
