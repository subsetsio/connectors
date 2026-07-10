-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "sppis_2021_100_according_to_nace_2008",
    "output_price_index_for_business_services"
FROM "statistics-austria-ogd-epidl21-epidl21-1"
