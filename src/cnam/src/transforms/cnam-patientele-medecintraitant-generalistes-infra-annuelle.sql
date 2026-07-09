-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A single in-progress-year snapshot (`annee` is constant, `date` is the end of the reference period), not a time series.
-- caution: `nombre_patients_medecin_traitant` is a mean per practitioner; the territory columns mix département, région and national rows.
SELECT
    "annee",
    "date",
    "profession_sante",
    CAST("region" AS BIGINT) AS region,
    "libelle_region",
    "departement",
    "libelle_departement",
    "nombre_patients_medecin_traitant",
    "taux_evolution_annuel"
FROM "cnam-patientele-medecintraitant-generalistes-infra-annuelle"
