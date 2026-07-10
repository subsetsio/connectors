-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "federal_states",
    "households_with_internet_access",
    "ict_specialists"
FROM "statistics-austria-ogd-desi-hh-mz-desi-hh-mz-1"
