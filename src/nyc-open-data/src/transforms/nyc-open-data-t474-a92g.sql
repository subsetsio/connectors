-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reported",
    "fiscal_year",
    "borough",
    "award",
    "council_district",
    "sponsor",
    "title",
    "description",
    "id",
    "budget_line"
FROM "nyc-open-data-t474-a92g"
