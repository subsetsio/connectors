SELECT
    TRY_CAST(row_id     AS INTEGER) AS row_id,
    TRY_CAST(study_id   AS INTEGER) AS study_id,
    TRY_CAST(year       AS INTEGER) AS year,
    TRY_CAST(month      AS INTEGER) AS month,
    TRY_CAST(day        AS INTEGER) AS day,
    NULLIF(sample_desc, 'NA')       AS sample_desc,
    NULLIF(plot, 'NA')              AS plot,
    TRY_CAST(id_species AS INTEGER) AS id_species,
    TRY_CAST(latitude   AS DOUBLE)  AS latitude,
    TRY_CAST(longitude  AS DOUBLE)  AS longitude,
    TRY_CAST(abundance  AS DOUBLE)  AS abundance,
    TRY_CAST(biomass    AS DOUBLE)  AS biomass,
    NULLIF(genus, 'NA')             AS genus,
    NULLIF(species, 'NA')           AS species,
    NULLIF(genus_species, 'NA')     AS genus_species
FROM "biotime-records"
WHERE TRY_CAST(study_id AS INTEGER) IS NOT NULL
