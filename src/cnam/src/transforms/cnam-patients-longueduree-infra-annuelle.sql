-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A single in-progress-year snapshot (`annee` is constant, `date` is the end of the reference period), not a time series.
-- caution: `taux_patients_ald_sans_mt` is a percentage; the territory columns mix département, région and national rows.
SELECT
    "annee",
    "date",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "taux_patients_ald_sans_mt"
FROM "cnam-patients-longueduree-infra-annuelle"
