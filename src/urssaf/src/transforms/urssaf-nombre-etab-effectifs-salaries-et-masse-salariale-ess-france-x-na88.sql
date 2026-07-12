-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "champ_ess",
    "famille_ess",
    "grand_secteur_d_activite",
    "secteur_na88",
    "annee",
    "nombre_d_etablissements",
    "effectifs_salaries_moyens",
    "masse_salariale"
FROM "urssaf-nombre-etab-effectifs-salaries-et-masse-salariale-ess-france-x-na88"
