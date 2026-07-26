-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "agency_name",
    "agency_acronym",
    "ecm_spend",
    "ecm_spend_1",
    "total_ad_spend"
FROM "nyc-open-data-9tn4-3mgm"
