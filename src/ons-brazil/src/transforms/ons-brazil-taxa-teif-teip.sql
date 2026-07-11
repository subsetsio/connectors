-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table carries TEIFa and TEIP measures in the same structure; filter nom_taxa before comparing rates.
SELECT
    "nom_usina",
    "cod_ceg",
    "tip_usina",
    "din_mes",
    "nom_taxa",
    "val_taxa",
    "num_versao",
    "din_calculo"
FROM "ons-brazil-taxa-teif-teip"
