-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEDICARE_PROV_NUM" AS medicare_prov_num,
    "ZIP_CD_OF_RESIDENCE" AS zip_cd_of_residence,
    "TOTAL_DAYS_OF_CARE" AS total_days_of_care,
    "TOTAL_CHARGES" AS total_charges,
    "TOTAL_CASES" AS total_cases
FROM "cms-8708ca8b-8636-44ed-8303-724cbfaf78ad"
