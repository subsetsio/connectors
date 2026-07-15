-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dollar" AS dollar,
    "Total" AS total,
    "IncomeQuintile1_1st_20th4" AS incomequintile1_1st_20th4,
    "IncomeQuintile1_21st_40th" AS incomequintile1_21st_40th,
    "IncomeQuintile1_41st_60th" AS incomequintile1_41st_60th,
    "IncomeQuintile1_61st_80th" AS incomequintile1_61st_80th,
    "IncomeQuintile1_81st_100th" AS incomequintile1_81st_100th
FROM "sg-data-d-a5523e2bf61e9719aa328984493c8247"
