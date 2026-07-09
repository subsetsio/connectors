-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "warnum",
    "disno",
    "dyindex",
    "statea",
    "stateb",
    "warstrtmnth",
    "warstrtday",
    "warstrtyr",
    "warendmnth",
    "warenday",
    "warendyr",
    "year",
    "warolea",
    "waroleb",
    "wardyadrolea",
    "wardyadroleb",
    "outcomea",
    "batdtha",
    "batdthb",
    "changes_1",
    "changes_2",
    "batdths",
    "durindx"
FROM "correlates-of-war-dyadic-interstate-war"
