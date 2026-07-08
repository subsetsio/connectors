SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    CAST(total AS INTEGER)      AS total_species,
    CAST(threatened AS INTEGER) AS threatened_species,
    categories                  AS categories_json
FROM "global-mangrove-watch-biodiversity"
