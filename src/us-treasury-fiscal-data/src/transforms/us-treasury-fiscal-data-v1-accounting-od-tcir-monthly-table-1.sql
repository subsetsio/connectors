-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "table_nm",
    "maturity",
    "previous_month_year",
    "rate_used_for_prev_month_year",
    "current_month_year",
    "rate_ind_for_curr_month_year",
    "rate_change",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr
FROM "us-treasury-fiscal-data-v1-accounting-od-tcir-monthly-table-1"
