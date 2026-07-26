-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "cost_category",
    "actualplan",
    "fiscal_year",
    "agency_code",
    "agency_name",
    "total_amount",
    "city_amount",
    "intracity_amount"
FROM "nyc-open-data-u42g-qjaj"
