-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "pass_loans",
    "sp_ment_loans",
    "cl_gross_substandard",
    "cl_gross_doubtful",
    "cl_gross_loss",
    "cl_gross_total",
    "cl_net",
    "loans_od3m",
    "loans_resch",
    "loans_od3m_resch_total",
    "cl_gross_mainland_lend"
FROM "hkma-asset-quality-ais"
