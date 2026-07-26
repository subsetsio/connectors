-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "economy",
    "economy_label",
    "governmentexpenditure",
    "governmentexpenditure_label",
    "us_dollars_at_current_prices_in_millions",
    "us_dollars_at_current_prices_in_millions_footnote",
    "us_dollars_at_current_prices_in_millions_missing_value",
    "percentage_of_gross_domestic_product",
    "percentage_of_gross_domestic_product_footnote",
    "percentage_of_gross_domestic_product_missing_value"
FROM "unctad-us.govexpenditures"
