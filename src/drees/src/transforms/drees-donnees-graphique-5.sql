-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tranche_d_age",
    "19901",
    "20001",
    "20141",
    "20191",
    "2020",
    "2021",
    "2022"
FROM "drees-donnees-graphique-5"
