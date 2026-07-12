-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    CAST("cip" AS BIGINT) AS cip,
    CAST("academic_year" AS BIGINT) AS academic_year,
    CAST("academic_year0" AS BIGINT) AS academic_year0,
    CAST("academic_year1" AS BIGINT) AS academic_year1,
    "cip_6_description",
    "cip_4_description",
    "cip_2_description",
    "stem",
    "high_demand"
FROM "washington-ofm-socrata-4x32-48q5"
