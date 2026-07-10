-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "nom_du_fichier",
    "url_de_telechargement"
FROM "drees-708-bases-statistiques-sae"
