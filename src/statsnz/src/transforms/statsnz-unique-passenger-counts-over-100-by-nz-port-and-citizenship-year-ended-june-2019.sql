-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "NZ Port" AS nz_port,
    "Citizenship" AS citizenship,
    CAST("Count" AS BIGINT) AS count,
    CAST("Year" AS BIGINT) AS year
FROM "statsnz-unique-passenger-counts-over-100-by-nz-port-and-citizenship-year-ended-june-2019"
