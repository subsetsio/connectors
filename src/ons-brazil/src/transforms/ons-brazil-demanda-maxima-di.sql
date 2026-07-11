-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "dat_referencia",
    "din_demandaintegralizada",
    "val_demandaintegralizada",
    "din_demandainstantanea",
    "val_demandainstantanea"
FROM "ons-brazil-demanda-maxima-di"
