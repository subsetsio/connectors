-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sub_boro_name",
    "borough",
    "fips",
    "unbanked_2011",
    "underbanked_2011",
    "unbanked_2013",
    "underbanked_2013",
    "prepaid_2011",
    "prepaid_2013",
    "foreign_born_2011",
    "poor_2011",
    "median_income_2011",
    "unemployment_2011",
    "poor_2013",
    "foreign_born_2013",
    "median_income_2013",
    "unemployment_2013"
FROM "nyc-open-data-v5w4-adxa"
