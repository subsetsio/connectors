-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Constrained-off detail rows include restriction origin and reason dimensions; filter those dimensions before aggregating curtailed energy.
SELECT
    "id_subsistema",
    "id_estado",
    "nom_modalidadeoperacao",
    "nom_conjuntousina",
    "nom_usina",
    "id_ons",
    "ceg",
    "din_instante",
    "val_irradianciaverificado",
    "flg_dadoirradianciainvalido",
    "val_geracaoestimada",
    "val_geracaoverificada"
FROM "ons-brazil-restricao-coff-fotovoltaica-detail"
