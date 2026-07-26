-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_date",
    "age_group",
    "engagement_category",
    "citywide_count"
FROM "nyc-open-data-pqmq-sk82"
