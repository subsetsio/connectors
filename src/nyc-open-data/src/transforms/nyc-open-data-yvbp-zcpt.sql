-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "published_date",
    "investment_area",
    "program_name",
    "description",
    "fiscal_year",
    "fiscal_year_amount",
    "remarks"
FROM "nyc-open-data-yvbp-zcpt"
