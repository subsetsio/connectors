-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "secteur_d_activite_me",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "immatriculations",
    "radiations",
    "economiquement_actifs",
    "administrativement_actifs",
    "chiffres_d_affaires"
FROM "urssaf-auto-entrepreneurs-par-secteur-dactivite"
