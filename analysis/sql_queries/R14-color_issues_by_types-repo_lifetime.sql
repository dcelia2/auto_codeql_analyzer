/*
WITH repo_base AS (
    SELECT
        r.id AS repo_id,
        (julianday(r.last_commit_date) - julianday(r.creation_date)) / 365.25 AS lifetime_years,
        SUM(er.occurrence_count) * 1000.0 / r.nb_lines AS issues_per_1000_lines
    FROM repos r
    JOIN error_reports er
        ON r.id = er.repo_id
    WHERE r.nb_lines > 0
    GROUP BY r.id
),
error_stats AS (
    SELECT
        r.id AS repo_id,
        ec.error_name,
        SUM(er.occurrence_count) AS error_count
    FROM repos r
    JOIN error_reports er
        ON r.id = er.repo_id
    JOIN error_catalog ec
        ON er.error_id = ec.error_id
    GROUP BY r.id, ec.error_name
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY repo_id
               ORDER BY error_count DESC
           ) AS rn
    FROM error_stats
)
SELECT
    b.repo_id,
    b.lifetime_years,
    b.issues_per_1000_lines,
    r.error_name AS dominant_error
FROM repo_base b
JOIN ranked r
    ON b.repo_id = r.repo_id
WHERE r.rn = 1;
*/

WITH repo_error_counts AS (
    SELECT
        r.id AS repo_id,
        (julianday(r.last_commit_date) - julianday(r.creation_date)) / 365.25 AS lifetime_years,
        r.nb_lines,
        ec.error_name,
        SUM(er.occurrence_count) AS error_count
    FROM repos r
    JOIN error_reports er
        ON r.id = er.repo_id
    JOIN error_catalog ec
        ON er.error_id = ec.error_id
    WHERE r.nb_lines > 0
      AND r.creation_date IS NOT NULL
      AND r.last_commit_date IS NOT NULL
    GROUP BY r.id, ec.error_name
),
repo_totals AS (
    SELECT
        repo_id,
        lifetime_years,
        nb_lines,
        SUM(error_count) AS total_errors
    FROM repo_error_counts
    GROUP BY repo_id
),
dominant AS (
    SELECT
        rec.repo_id,
        rec.lifetime_years,
        rec.error_name,
        rec.error_count,
        rt.nb_lines,
        rt.total_errors,
        (rec.error_count * 1.0 / rt.total_errors) AS ratio,
        ROW_NUMBER() OVER (
            PARTITION BY rec.repo_id
            ORDER BY rec.error_count DESC
        ) AS rn
    FROM repo_error_counts rec
    JOIN repo_totals rt
        ON rec.repo_id = rt.repo_id
)
SELECT
    repo_id,
    lifetime_years,
    (total_errors * 1000.0 / nb_lines) AS issues_per_1000_lines,
    CASE
        WHEN ratio >= 0.3 THEN error_name
        ELSE 'Other'
    END AS dominant_error
FROM dominant
WHERE rn = 1;
