-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    "cod_pontoconexao",
    "nom_pontoconexao",
    "nom_localizacao",
    "val_latitudesecoletora",
    "val_longitudesecoletora",
    "val_latitudepontoconexao",
    "val_longitudepontoconexao",
    "nom_modalidadeoperacao",
    "nom_tipousina",
    "nom_usina_conjunto",
    "id_ons",
    "ceg",
    "din_instante",
    "val_geracaoprogramada",
    "val_geracaoverificada",
    "val_capacidadeinstalada",
    "val_fatorcapacidade"
FROM "ons-brazil-fator-capacidade-2"
