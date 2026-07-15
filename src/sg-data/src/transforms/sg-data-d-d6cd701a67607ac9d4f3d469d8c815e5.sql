-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "actual_revised_estimated",
    "class",
    "type",
    "amount_in_millions",
    "percent_of_gdp"
FROM "sg-data-d-d6cd701a67607ac9d4f3d469d8c815e5"
