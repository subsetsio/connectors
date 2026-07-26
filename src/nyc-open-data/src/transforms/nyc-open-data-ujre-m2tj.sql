-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "post_date",
    "mocs_award_number",
    "agency",
    "vendor_name",
    "amount",
    "_source" AS source,
    "statussummary"
FROM "nyc-open-data-ujre-m2tj"
