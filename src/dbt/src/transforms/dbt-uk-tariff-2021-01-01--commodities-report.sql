-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("commodity__sid" AS BIGINT) AS commodity_sid,
    "commodity__code" AS commodity_code,
    CAST("commodity__suffix" AS BIGINT) AS commodity_suffix,
    "commodity__description" AS commodity_description,
    "commodity__validity_start" AS commodity_validity_start,
    "commodity__validity_end" AS commodity_validity_end,
    "parent__sid" AS parent_sid,
    "parent__code" AS parent_code,
    "parent__suffix" AS parent_suffix
FROM "dbt-uk-tariff-2021-01-01--commodities-report"
