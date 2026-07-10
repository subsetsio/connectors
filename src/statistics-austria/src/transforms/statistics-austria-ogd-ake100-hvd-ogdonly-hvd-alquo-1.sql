-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_series",
    "quota_classifications",
    "unemployment_rate_15_to_74_years",
    "long_term_unemployment_rate_15_to_74_years"
FROM "statistics-austria-ogd-ake100-hvd-ogdonly-hvd-alquo-1"
