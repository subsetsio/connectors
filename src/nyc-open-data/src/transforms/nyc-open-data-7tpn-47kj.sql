-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "revenue_source",
    "grant_name",
    "current_award_total",
    "collected_earned_revenue"
FROM "nyc-open-data-7tpn-47kj"
