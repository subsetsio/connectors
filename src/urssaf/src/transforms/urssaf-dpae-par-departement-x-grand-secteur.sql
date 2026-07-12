-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "ancienne_region",
    "departement",
    "grand_secteur_d_activite",
    "duree_de_contrat",
    "nature_de_contrat",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "code_region",
    "code_ancienne_region",
    "code_departement",
    "dpae_brut",
    "dpae_cvs"
FROM "urssaf-dpae-par-departement-x-grand-secteur"
