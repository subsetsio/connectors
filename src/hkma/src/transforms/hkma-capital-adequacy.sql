-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_quarter", '%Y-%m')::DATE AS end_of_quarter,
    "com_eqt_t1cap_ratio",
    "t1cap_ratio",
    "total_cap_ratio",
    "leverage_ratio"
FROM "hkma-capital-adequacy"
