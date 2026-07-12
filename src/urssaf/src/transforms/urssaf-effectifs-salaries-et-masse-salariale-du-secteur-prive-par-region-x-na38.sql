-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "ancienne_region",
    "grand_secteur_d_activite",
    "secteur_na28i",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "code_region",
    "code_ancienne_region",
    "effectifs_salaries_brut",
    "effectifs_salaries_cvs",
    "masse_salariale_brut",
    "masse_salariale_cvs"
FROM "urssaf-effectifs-salaries-et-masse-salariale-du-secteur-prive-par-region-x-na38"
