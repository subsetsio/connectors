-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "EPT" AS ept,
    "NB_EPL_TRANCHES" AS nb_epl_tranches,
    "SURFACE_TRANCHES" AS surface_tranches,
    "DENSITE_TRANCHES" AS densite_tranches
FROM "sdes-c380b36e-e665-4195-870b-936893532431"
