-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    "categ_r",
    "region_code_r",
    CAST("sexe" AS BIGINT) AS sexe,
    "age",
    CAST("majpro" AS BIGINT) AS majpro,
    "defp_r",
    "limitq1",
    "limitq2",
    "limitq3",
    "limitq4",
    "limitq5",
    "limitq6",
    "limitq7",
    "limitq8",
    "limitq9",
    "limitq10",
    "limitq11",
    "limitq12",
    "aduacti",
    "aduheberg",
    "tps_presence_mois",
    "meme_dep",
    "poids_pers",
    "poids_dc"
FROM "drees-adultes-presents-es-handicap-2022-base-floutee-v1"
