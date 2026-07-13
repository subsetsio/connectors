-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include United Kingdom and country-level geographies; filter COUNTRY before aggregating or comparing regional series.
SELECT
    "SPECIES_CODE" AS species_code,
    "SPECIES" AS species,
    "COMMON_NAME" AS common_name,
    "YEAR" AS year,
    "N_SITES" AS n_sites,
    "COLLATED_INDEX" AS collated_index,
    "YEAR_RANK" AS year_rank,
    "TIME_PERIOD" AS time_period,
    "COUNTRY" AS country
FROM "ukbms-collated-indices-2024"
