-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("quota_definition__sid" AS BIGINT) AS quota_definition_sid,
    CAST("idx" AS BIGINT) AS idx,
    "heading"
FROM "dbt-uk-trade-quotas--quota--headings"
