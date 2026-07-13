-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Championship rows describe championship classifications and eligibility, not individual competition results.
SELECT
    CAST("id" AS BIGINT) AS id,
    "competition_id",
    "championship_type",
    "_source_table" AS source_table,
    CAST("_export_date" AS TIMESTAMP) AS export_date,
    "_export_version" AS export_version
FROM "wca-championships"
