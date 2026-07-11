-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "ID_AIRE" AS id_aire,
    "NOM_AIRE" AS nom_aire,
    "NB_EPL_TRANCHES" AS nb_epl_tranches,
    "SURFACE_TRANCHES" AS surface_tranches
FROM "sdes-7f468d42-37dd-44c9-b5f0-b594d5f17fba"
