-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One `record_date` carries many `calendar_year` rows — `calendar_year` is part of the row identity, because each publication restates a whole block of years. Filter or group by `calendar_year` before aggregating.
SELECT
    "record_date",
    "table_nm",
    "legislation",
    CAST(NULLIF("calendar_year", 'null') AS BIGINT) AS calendar_year,
    "calendar_year_rate",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr
FROM "us-treasury-fiscal-data-v1-accounting-od-tcir-annual-table-7"
