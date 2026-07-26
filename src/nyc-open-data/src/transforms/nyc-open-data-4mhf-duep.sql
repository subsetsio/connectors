-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "zip_code_tabulation_area_zcta_2020",
    "heat_vulnerability_index_hvi"
FROM "nyc-open-data-4mhf-duep"
