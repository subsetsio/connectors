-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "nombre_de_lits_d_hospitalisation_complete_echelle_de_gauche",
    "nombre_de_places_d_hospitalisation_partielle_echelle_de_droite"
FROM "drees-graphique-1-evolution-du-nombre-de-lits-et-de-places-au-31-decembre-depuis-fin-2013"
