SELECT
    CAST(id AS INTEGER)               AS id,
    country                           AS country_name_short,
    CAST(start_date AS DATE)          AS start_date,
    party                             AS party_name_short,
    pm = 'True'                       AS prime_minister,
    defector = 'True'                 AS defector,
    party_id_source,
    CAST(cabinet_id AS INTEGER)       AS cabinet_id,
    CAST(party_id AS INTEGER)         AS party_id
FROM "parlgov-view-cabinet"
