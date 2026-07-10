-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("field_id" AS BIGINT) AS field_id,
    "field_name",
    "field_sector_id",
    CAST("field_rank" AS BIGINT) AS field_rank
FROM "epo-fields"
