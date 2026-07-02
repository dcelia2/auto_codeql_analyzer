-- Table classant les différents types d'erreur par
-- nombre d'apparition (sur tous les repos) décroissant,
-- y compris celles jamais observées.

SELECT
    ec.error_name,
    COALESCE(SUM(er.occurrence_count), 0) AS total_occurrences
FROM error_catalog ec
LEFT JOIN error_reports er
    ON ec.error_id = er.error_id
GROUP BY ec.error_id, ec.error_name
ORDER BY total_occurrences DESC;
