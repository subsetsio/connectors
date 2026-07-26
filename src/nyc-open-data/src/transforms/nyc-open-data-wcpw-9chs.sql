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
    "four_year_cost",
    "first_of_six_years",
    "six_year_cost"
FROM "nyc-open-data-wcpw-9chs"
