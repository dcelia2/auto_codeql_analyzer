.print ====================================
.print          General statistics
.print ====================================
.print


-- Number of repositories analysed
.print Number of repositories analysed:
          SELECT COUNT(*) FROM repos;
.print ____________________________________

-- Number of repositories present in the initial .json file
-- To obtain this:
        -- Go to the analysis folder
        -- Type the following into the console: jq “length” android-apps.json
        -- The result displayed is the number of repositories

-- Creation period of the analysed repositories
.print Creation period of the analysed repositories:
          SELECT 
              MIN(creation_date) || ' - ' || MAX(creation_date)
          FROM repos;
.print ____________________________________


-- Period of the most recent updates to the analysed repositories
.print Period of the most recent updates to the analysed repositories:
          SELECT
             MIN(last_commit_date) || ' - ' || MAX(last_commit_date)
          FROM repos;
.print ____________________________________

-- Average lifespan of a project 
.print Average lifespan of a project (in years):
          SELECT AVG((julianday(last_commit_date) - julianday(creation_date)) / 365.25)
          FROM repos
          WHERE creation_date IS NOT NULL
            AND last_commit_date IS NOT NULL;
.print ____________________________________


-- Number of different issue types
.print Number of different issue types:
          SELECT COUNT(*) FROM error_catalog;
.print ____________________________________

-- Number of different categories
.print Number of different categories:
          SELECT COUNT(DISTINCT category) FROM repo_categories;
.print ____________________________________

-- Total number of issues found
.print Total number of issues found:
        SELECT SUM(occurrence_count) AS total_errors
        FROM error_reports;
.print ____________________________________

-- Average number of lines in repos
.print Average number of lines in the analysed repos:
        SELECT AVG(nb_lines)
        FROM repos
        WHERE nb_lines > 0;
.print ____________________________________

-- Repos with 0 issues:

        -- Number of repos with 0 issues
.print Number of repos with 0 issues:
        SELECT COUNT(*) FROM repos
          WHERE id NOT IN (
              SELECT DISTINCT repo_id
              FROM error_reports
          );
.print ____________________________________


        -- Average number of lines
.print Average number of lines in repositories with 0 issues:
          SELECT AVG(nb_lines) FROM repos
          WHERE id NOT IN (
              SELECT DISTINCT repo_id FROM error_reports
        );
.print _____________________________________

        -- Average number of stars
.print Average number of stars for repositories with 0 issues:
          SELECT AVG(stars) FROM repos
          WHERE id NOT IN (
              SELECT DISTINCT repo_id FROM error_reports
          );
.print _____________________________________

        -- Average date of last update:
.print Average date of last update for repositories with 0 issues:
        SELECT DATE(AVG(julianday(last_commit_date)))  FROM repos
        WHERE id NOT IN (
            SELECT DISTINCT repo_id
            FROM error_reports
        );
.print _____________________________________

-- Repositories with at least 1 issue:

        -- Average number of lines:
.print Average number of lines in repositories with 1 or more issues:
        SELECT AVG(nb_lines)  FROM repos
        WHERE id IN (
            SELECT DISTINCT repo_id
            FROM error_reports
        );
.print ____________________________________

        -- Average number of stars
.print Average number of stars for repositories with 1 or more issues:
        SELECT AVG(stars)  FROM repos
        WHERE id IN (
            SELECT DISTINCT repo_id
            FROM error_reports
        );
.print ____________________________________

        -- Average date of last update
.print Average date of last update for repos with at least 1 issue:
        SELECT DATE(AVG(julianday(last_commit_date)))  FROM repos
        WHERE id IN (
            SELECT DISTINCT repo_id
            FROM error_reports
        );
.print ____________________________________

-- ‘Missing ...’ issues
.print Number of repositories with a ‘Missing ...’ issue
        SELECT COUNT(DISTINCT er.repo_id)
        FROM error_reports er
        JOIN error_catalog ec
            ON er.error_id = ec.error_id
        WHERE ec.error_name LIKE 'Missing%';
.print ____________________________________


.print Total number of ‘Missing’ issues found
        SELECT SUM(er.occurrence_count)
        FROM error_reports er
        JOIN error_catalog ec
            ON er.error_id = ec.error_id
        WHERE ec.error_name LIKE 'Missing%';
.print ____________________________________

        -- Average number of lines
.print Average number of lines in repositories with at least one ‘Missing ...’ issue
        SELECT AVG(nb_lines)
        FROM repos
        WHERE id IN (
            SELECT DISTINCT er.repo_id
            FROM error_reports er
            JOIN error_catalog ec
                ON er.error_id = ec.error_id
            WHERE ec.error_name LIKE 'Missing%'
        );
.print ____________________________________

.print Average number of lines in repos with no ‘Missing ...’ issue
        SELECT AVG(nb_lines)
        FROM repos
        WHERE id NOT IN (
            SELECT DISTINCT er.repo_id
            FROM error_reports er
            JOIN error_catalog ec
                ON er.error_id = ec.error_id
            WHERE ec.error_name LIKE 'Missing%'
        );
.print ____________________________________
.print
.print

