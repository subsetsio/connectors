SELECT
    CAST(id AS INTEGER)       AS id,
    description,
    CAST(type_id AS INTEGER)  AS type_id,
    CAST(party_id AS INTEGER) AS party_id
FROM "parlgov-data-party-family"

