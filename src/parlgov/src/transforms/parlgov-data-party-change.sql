SELECT
    CAST(id AS INTEGER)          AS id,
    CAST(date AS DATE)           AS change_date,
    data_source,
    description,
    CAST(party_id AS INTEGER)    AS party_id,
    CAST(party_id_new AS INTEGER) AS party_id_new,
    CAST(type_id AS INTEGER)     AS type_id
FROM "parlgov-data-party-change"

