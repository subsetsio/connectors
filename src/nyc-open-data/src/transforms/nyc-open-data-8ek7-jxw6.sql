-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator_id",
    "indicator_name",
    "_domain" AS domain,
    "agency_name",
    "dimension_category",
    "dimension",
    "industry",
    "interval",
    "period",
    "unit",
    "_value" AS value
FROM "nyc-open-data-8ek7-jxw6"
