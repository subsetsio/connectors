-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "overseas_incorp_ais",
    "locally_incorp_ais",
    "mainland_bank_subs_ais",
    "lending_total"
FROM "hkma-mainland-lending-ais"
