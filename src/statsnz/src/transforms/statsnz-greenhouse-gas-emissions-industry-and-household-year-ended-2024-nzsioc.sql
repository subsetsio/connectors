-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "nzsioc",
    "nzsioc_descriptor",
    "nzsioc_descriptor2",
    "variable",
    "units",
    "magnitude",
    "source",
    "data_value"
FROM "statsnz-greenhouse-gas-emissions-industry-and-household-year-ended-2024-nzsioc"
