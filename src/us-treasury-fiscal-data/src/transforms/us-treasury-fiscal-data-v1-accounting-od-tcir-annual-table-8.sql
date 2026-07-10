-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One `record_date` carries many `fiscal_year` rows — `fiscal_year` is part of the row identity, because each publication restates a whole block of years. Filter or group by `fiscal_year` before aggregating.
SELECT
    "record_date",
    "table_nm",
    "legislation",
    CAST(NULLIF("fiscal_year", 'null') AS BIGINT) AS fiscal_year,
    "fiscal_year_rate",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr
FROM "us-treasury-fiscal-data-v1-accounting-od-tcir-annual-table-8"
