-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grand_secteur_d_activite",
    "secteur_na38",
    "duree_de_contrat",
    "nature_de_contrat",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "dpae_brut",
    "dpae_cvs"
FROM "urssaf-dpae-france-entiere-x-na38"
