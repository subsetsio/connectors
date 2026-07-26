-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unique_key",
    "account",
    "open_date",
    "complaint_type",
    "descriptor",
    "zip",
    "borough",
    "city",
    "council_district",
    "community_board",
    "close_date"
FROM "nyc-open-data-b9km-gdpy"
