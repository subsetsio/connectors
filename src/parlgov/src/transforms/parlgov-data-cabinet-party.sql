SELECT
    CAST(id AS INTEGER)               AS id,
    pm = 'True'                       AS prime_minister,
    defector = 'True'                 AS defector,
    party_id_source,
    CAST(cabinet_id AS INTEGER)       AS cabinet_id,
    CAST(party_id AS INTEGER)         AS party_id
FROM "parlgov-data-cabinet-party"
