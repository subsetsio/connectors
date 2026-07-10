-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_series" AS BIGINT) AS time_series,
    "employment_by_industry_persons_domestic_concept",
    "total",
    "employees",
    "self_employed"
FROM "statistics-austria-ogd-vgr110-vgr-personen-1"
