-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "trimestre",
    "dernier_jour_du_mois",
    "duree_de_contrat",
    "nature_de_contrat",
    "dpae_brut",
    "dpae_cvs"
FROM "urssaf-dpae-mensuelles-france-entiere"
