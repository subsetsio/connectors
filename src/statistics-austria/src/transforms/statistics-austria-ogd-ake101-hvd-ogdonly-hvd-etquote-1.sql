-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_series",
    "quota_classifications",
    "part_time_employment_rate_20_to_64_years",
    "employment_rate_20_to_64_years"
FROM "statistics-austria-ogd-ake101-hvd-ogdonly-hvd-etquote-1"
