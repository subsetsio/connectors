-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "service_title",
    "total_transactions",
    "successful_transactions",
    "page_url",
    "service_action_url"
FROM "qatar-planning-and-statistics-authority-e-government-services-transactions-hukoomi-by-year"
