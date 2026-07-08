SELECT
    CAST(id AS INTEGER)               AS id,
    name                              AS cabinet_name,
    CAST(start_date AS DATE)          AS start_date,
    CAST(termination_date AS DATE)    AS termination_date,
    caretaker = 'True'                AS caretaker,
    CAST(country_id AS INTEGER)       AS country_id,
    CAST(election_id AS INTEGER)      AS election_id,
    wikipedia,
    data_source
FROM "parlgov-data-cabinet"
