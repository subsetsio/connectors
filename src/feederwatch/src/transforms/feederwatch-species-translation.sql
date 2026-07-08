SELECT
    species_code,
    alt_full_spp_code,
    TRY_CAST(n_locations AS INTEGER)          AS n_locations,
    scientific_name,
    american_english_name,
    TRY_CAST(taxonomy_version AS INTEGER)     AS taxonomy_version,
    TRY_CAST(taxonomic_sort_order AS DOUBLE)  AS taxonomic_sort_order
FROM "feederwatch-species-translation"
WHERE species_code IS NOT NULL
