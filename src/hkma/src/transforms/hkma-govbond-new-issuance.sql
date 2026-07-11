-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "institutional_1y",
    "institutional_2y",
    "institutional_3y",
    "institutional_5y",
    "institutional_10y",
    "institutional_15y",
    "institutional_20y",
    "institutional_subtotal",
    "retail_3y",
    "retail_subtotal",
    "total"
FROM "hkma-govbond-new-issuance"
