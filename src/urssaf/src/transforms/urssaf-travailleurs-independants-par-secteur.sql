-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_de_travailleur_independant",
    "groupe_professionnel",
    "secteur_d_activite",
    "annee",
    "administrativement_actifs",
    "economiquement_actifs"
FROM "urssaf-travailleurs-independants-par-secteur"
