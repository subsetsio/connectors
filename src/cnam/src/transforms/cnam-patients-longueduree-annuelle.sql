-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `taux_patients_ald_sans_mt` is the share of long-term-condition (ALD) patients without a declared attending physician — a percentage, never summable.
-- caution: The territory columns mix département, région and national rows.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "taux_patients_ald_sans_mt",
    "taux_patients_ald_sans_mt_integer"
FROM "cnam-patients-longueduree-annuelle"
