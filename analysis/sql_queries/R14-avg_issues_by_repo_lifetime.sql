
    SELECT 
        r.id,
        (julianday(r.last_commit_date) - julianday(r.creation_date)) / 365.25 AS lifetime_years,
        (SUM(er.occurrence_count)*1000.0/ r.nb_lines) AS issues_per_1000_lines
    FROM repos r
    JOIN error_reports er
        ON r.id = er.repo_id
    WHERE r.creation_date IS NOT NULL
      AND r.last_commit_date IS NOT NULL
      AND r.nb_lines>0
    GROUP BY r.id, r.creation_date, r.last_commit_date, r.nb_lines
    ORDER BY lifetime_years;
