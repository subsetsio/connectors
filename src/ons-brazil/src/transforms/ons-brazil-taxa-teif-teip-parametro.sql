-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Parameter rows represent operating-hour components used in TEIFa and TEIP calculations; do not aggregate them as final rates.
SELECT
    "nom_usina",
    "id_tipousina",
    "nom_unidadegeradora",
    "cod_ceg",
    "dat_periodo",
    "nom_tpinsumo",
    "val_parametro",
    "num_versao",
    "din_parametro"
FROM "ons-brazil-taxa-teif-teip-parametro"
