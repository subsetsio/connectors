-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "industries_nace_and_size_classes",
    "turnover_with_product_innovations_in_ml_euro",
    "turnover_with_product_innovations_as_of_total_turnover",
    "turnover_with_product_innovations_in_ml_euro_of_which_market_novelties",
    "turnover_with_market_novelties_as_of_total_turnover",
    "turnover_with_product_innovations_in_ml_euro_of_which_products_only_new_to_the_firm",
    "turnover_with_product_innovations_only_new_to_the_firm_as_of_total_turnover"
FROM "statistics-austria-ogd-innov004-cis-004-unt-innovation-1"
