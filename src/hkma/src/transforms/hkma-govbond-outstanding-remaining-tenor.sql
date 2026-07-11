-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "institutional_1y_or_below",
    "institutional_1yto3y",
    "institutional_3yto5y",
    "institutional_5yto7y",
    "institutional_over7y",
    "institutional_subtotal",
    "retail_1y_or_below",
    "retail_1yto3y",
    "retail_3yto5y",
    "retail_5yto7y",
    "retail_subtotal",
    "total"
FROM "hkma-govbond-outstanding-remaining-tenor"
