-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "variable",
    "date",
    "employed",
    "employed_employer",
    "employed_employee",
    "employed_own_account",
    "employed_unpaid_family"
FROM "dosm-lfs-month-status"
