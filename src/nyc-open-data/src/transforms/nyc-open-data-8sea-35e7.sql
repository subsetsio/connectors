-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "agency_number",
    "agency_name",
    "discipline_or_system",
    "first_of_four_years",
    "fiscal_year_1_amount",
    "fiscal_year_2_amount",
    "fiscal_year_3_amount",
    "fiscal_year_4_amount"
FROM "nyc-open-data-8sea-35e7"
