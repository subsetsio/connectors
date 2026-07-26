-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "facility",
    "report_start_date",
    strptime("report_end_date", '%m/%d/%Y')::DATE AS report_end_date,
    "number"
FROM "nyc-open-data-mpqk-skis"
