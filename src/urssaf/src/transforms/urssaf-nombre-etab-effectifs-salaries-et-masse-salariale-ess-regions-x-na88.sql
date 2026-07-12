-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "champ_ess",
    "famille_ess",
    "secteur_na88",
    "annee",
    "code_region",
    "nombre_d_etablissements",
    "effectifs_salaries_moyens",
    "masse_salariale"
FROM "urssaf-nombre-etab-effectifs-salaries-et-masse-salariale-ess-regions-x-na88"
