-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("reference_date", '%Y-%m-%d')::DATE AS reference_date,
    "users_1_day",
    "users_7_days",
    "users_14_days",
    "users_28_days",
    "users_30_days",
    "new_users"
FROM "base-dos-dados-br-bd-indicadores--website-user"
