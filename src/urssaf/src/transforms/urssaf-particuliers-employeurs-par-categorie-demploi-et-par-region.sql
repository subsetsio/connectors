-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "ancienne_region",
    "categorie_d_emploi",
    "type_d_emploi",
    "systeme_declaratif",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "code_region",
    "code_ancienne_region",
    "code_categorie_d_emploi",
    "nombre_d_employeurs_brut",
    "nombre_d_heures_declarees_brut",
    "masse_salariale_nette_brut",
    "nombre_d_employeurs_cvs",
    "nombre_d_heures_declarees_cvs",
    "masse_salariale_nette_cvs"
FROM "urssaf-particuliers-employeurs-par-categorie-demploi-et-par-region"
