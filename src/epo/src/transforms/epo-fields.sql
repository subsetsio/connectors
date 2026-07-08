SELECT
    CAST(field_id AS INTEGER)   AS field_id,
    field_name,
    field_sector_id,
    CAST(field_rank AS INTEGER) AS field_rank
FROM "epo-fields"
