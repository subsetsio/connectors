-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A single in-progress-year snapshot (`annee` is constant, `date` is the end of the reference period), not a time series.
-- caution: `nombre_patients_uniques` is a mean per practitioner, not a total; the territory columns mix département, région and national rows.
SELECT
    "annee",
    "date",
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "nombre_patients_uniques",
    "taux_evolution_annuel",
    "taux_evolution_annuel_integer"
FROM "cnam-file-active-medgen-infra-annuelle"
