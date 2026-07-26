-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "agency_code",
    "agency_name",
    "all_funds",
    "city_fund",
    "remark"
FROM "nyc-open-data-7yay-m4ae"
