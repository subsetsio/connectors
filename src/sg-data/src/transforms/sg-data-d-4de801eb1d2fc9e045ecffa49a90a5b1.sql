-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PerCent" AS percent,
    "Total" AS total,
    "IncomeQuintile2_1st_20th3" AS incomequintile2_1st_20th3,
    "IncomeQuintile2_21st_40th" AS incomequintile2_21st_40th,
    "IncomeQuintile2_41st_60th" AS incomequintile2_41st_60th,
    "IncomeQuintile2_61st_80th" AS incomequintile2_61st_80th,
    "IncomeQuintile2_81st_100th" AS incomequintile2_81st_100th
FROM "sg-data-d-4de801eb1d2fc9e045ecffa49a90a5b1"
