-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table carries several robustness indicators and aggregation levels; filter the characteristic and aggregation columns before comparing values.
SELECT
    "cod_indicador",
    "dsc_agregacao",
    "cod_caracteristica",
    "dsc_caracteristica",
    "id_periodicidade",
    "din_referencia",
    "val_indicador",
    "num_perturbacoes",
    "num_perturbacoescortecarga",
    "num_perturbacoescortecarga_0a50mw",
    "num_perturbacoescortecarga_50a100mw",
    "num_perturbacoescortecarga_maior100mw"
FROM "ons-brazil-ind-confiarb-robustez"
