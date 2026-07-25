-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("segment_id" AS BIGINT) AS segment_id,
    "segment_name",
    CAST("seg_terminal1_id" AS BIGINT) AS seg_terminal1_id,
    CAST("seg_terminal2_id" AS BIGINT) AS seg_terminal2_id,
    CAST("seg_type" AS BIGINT) AS seg_type,
    CAST("serves_nps" AS BOOLEAN) AS serves_nps,
    CAST("census_year" AS BIGINT) AS census_year,
    CAST("data_year" AS BIGINT) AS data_year
FROM "u-s-department-of-transportation-gn77-pp24"
