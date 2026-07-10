-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee_de_parution" AS BIGINT) AS annee_de_parution,
    "ndeg_er",
    "titre",
    "url_de_telechargement_des_donnees",
    "url_vers_la_publication"
FROM "drees-etudes-et-resultats"
