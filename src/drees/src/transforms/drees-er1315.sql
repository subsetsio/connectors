-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "nombre_de_lits_d_hospitalisation_complete",
    "nombre_de_places_d_hospitalisation_partielle"
FROM "drees-er1315"
