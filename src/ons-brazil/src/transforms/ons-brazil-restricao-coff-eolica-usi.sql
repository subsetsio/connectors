-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Constrained-off rows include curtailment reason and availability dimensions; keep those fields distinct when aggregating.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    "nom_usina",
    "id_ons",
    "ceg",
    "din_instante",
    CAST("val_geracao" AS DOUBLE) AS val_geracao,
    "val_geracaolimitada",
    CAST("val_disponibilidade" AS DOUBLE) AS val_disponibilidade,
    CAST("val_geracaoreferencia" AS DOUBLE) AS val_geracaoreferencia,
    "val_geracaoreferenciafinal",
    "cod_razaorestricao",
    "cod_origemrestricao",
    "dsc_restricao"
FROM "ons-brazil-restricao-coff-eolica-usi"
