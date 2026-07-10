-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "HOSP_ID" AS hosp_id,
    "ADM_DISC" AS adm_disc,
    "RATE" AS rate,
    "INTERVAL_LOWER_LIMIT" AS interval_lower_limit,
    "INTERVAL_HIGHER_LIMIT" AS interval_higher_limit,
    "START_QUARTER" AS start_quarter,
    "START_DATE" AS start_date,
    "END_QUARTER" AS end_quarter,
    strptime("END_DATE", '%m/%d/%Y')::DATE AS end_date
FROM "cms-7cf9662e-7c5c-4fe0-a8c6-828edf81a23c"
