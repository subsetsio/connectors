-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("described_footnote_id" AS BIGINT) AS described_footnote_id,
    CAST("sid" AS BIGINT) AS sid,
    "validity_start",
    "description"
FROM "dbt-uk-tariff-2021-01-01--footnote-descriptions"
