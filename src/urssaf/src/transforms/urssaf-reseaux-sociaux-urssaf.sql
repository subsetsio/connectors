-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "libelle_organisme",
    "reseau_social",
    "services",
    "url_reseau"
FROM "urssaf-reseaux-sociaux-urssaf"
