SELECT
    CAST(race_id AS BIGINT)         AS race_id,
    CAST(title AS VARCHAR)          AS title,
    CAST(office AS VARCHAR)         AS office,
    TRY_CAST(year AS INTEGER)       AS year,
    CAST(state AS VARCHAR)          AS state,
    CAST(country AS VARCHAR)        AS country,
    CAST(category AS VARCHAR)       AS category,
    CAST(slug AS VARCHAR)           AS slug,
    CAST(fullpath AS VARCHAR)       AS fullpath,
    CAST(link AS VARCHAR)           AS link,
    CAST(num_candidates AS INTEGER) AS num_candidates,
    CAST(candidate_names AS VARCHAR) AS candidate_names,
    CAST(num_polls AS INTEGER)      AS num_polls,
    CAST(last_build_date AS VARCHAR) AS last_build_date
FROM "realclearpolitics-races"
WHERE race_id IS NOT NULL
