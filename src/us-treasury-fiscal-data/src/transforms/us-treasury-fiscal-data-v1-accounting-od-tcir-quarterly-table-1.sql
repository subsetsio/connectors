-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One `record_date` carries many `year` rows — `year` is part of the row identity, because each publication restates a whole block of years. Filter or group by `year` before aggregating.
SELECT
    "record_date",
    "table_nm",
    "month",
    CAST(NULLIF("year", 'null') AS BIGINT) AS year,
    CAST(NULLIF("dollar_amt_sold", 'null') AS DOUBLE) AS dollar_amt_sold,
    "avg_yield_to_maturity",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr
FROM "us-treasury-fiscal-data-v1-accounting-od-tcir-quarterly-table-1"
