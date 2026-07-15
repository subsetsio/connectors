-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dollar" AS dollar,
    "Total" AS total,
    "ExpenditureQuintile1_1st_20th" AS expenditurequintile1_1st_20th,
    "ExpenditureQuintile1_21st_40th" AS expenditurequintile1_21st_40th,
    "ExpenditureQuintile1_41st_60th" AS expenditurequintile1_41st_60th,
    "ExpenditureQuintile1_61st_80th" AS expenditurequintile1_61st_80th,
    "ExpenditureQuintile1_81st_100th" AS expenditurequintile1_81st_100th
FROM "sg-data-d-76ac49051fb05459b517a117dffa92ce"
