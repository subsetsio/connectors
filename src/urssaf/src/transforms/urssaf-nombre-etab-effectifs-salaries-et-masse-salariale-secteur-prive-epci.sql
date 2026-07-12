-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "ancienne_region",
    "epci",
    "annee",
    "code_region",
    "code_ancienne_region",
    "code_epci",
    "nombre_d_etablissements",
    "effectifs_salaries_moyens",
    "masse_salariale"
FROM "urssaf-nombre-etab-effectifs-salaries-et-masse-salariale-secteur-prive-epci"
