-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("reporting_year" AS BIGINT) AS reporting_year,
    "marriages_establishment_of_registered_partnerships",
    "sex_of_partners",
    "number"
FROM "statistics-austria-ogd-eheepext-ehe-epa-1"
