-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source contains repeated site/species/year records, including duplicate rows and some repeated rows with different SITE_INDEX sentinel values; do not assume one row per site/species/year.
SELECT
    "SITE_CODE" AS site_code,
    "COUNTRY" AS country,
    "SPECIES_CODE" AS species_code,
    "SPECIES" AS species,
    "COMMON_NAME" AS common_name,
    "YEAR" AS year,
    "SITE_INDEX" AS site_index
FROM "ukbms-site-indices-2024"
