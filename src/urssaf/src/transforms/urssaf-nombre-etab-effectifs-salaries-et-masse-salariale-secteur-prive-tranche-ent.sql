-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tranche_d_effectif",
    "annee",
    "nombre_d_entreprises",
    "nombre_d_etablissements",
    "effectifs_salaries_moyens",
    "masse_salariale"
FROM "urssaf-nombre-etab-effectifs-salaries-et-masse-salariale-secteur-prive-tranche-ent"
