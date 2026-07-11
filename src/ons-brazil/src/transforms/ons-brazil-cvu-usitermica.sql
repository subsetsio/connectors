-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dat_iniciosemana",
    "dat_fimsemana",
    "ano_referencia",
    "mes_referencia",
    "num_revisao",
    "nom_semanaoperativa",
    "cod_usinaplanejamento",
    "id_subsistema",
    "nom_subsistema",
    "nom_usina",
    "val_cvu"
FROM "ons-brazil-cvu-usitermica"
