-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "categorie_d_offre_de_service",
    "libelle_court_du_service",
    "libelle_long_du_service",
    "numero_de_telephone",
    "statut",
    "date_de_mise_a_jour"
FROM "urssaf-numero-de-telephone-des-services-cotisants"
