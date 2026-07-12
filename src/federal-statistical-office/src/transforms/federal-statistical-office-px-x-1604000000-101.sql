-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "internetzugang",
    "sprachgebiet",
    "haushaltsgrösse" AS haushaltsgr_sse,
    "subjektive_finanzielle_situation_des_haushalts",
    CAST("jahr" AS BIGINT) AS jahr,
    "absolut_relativ",
    "resultat",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1604000000-101"
