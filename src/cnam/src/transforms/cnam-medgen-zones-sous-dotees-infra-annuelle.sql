-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A single in-progress-year snapshot (`annee` is constant, `date` is the end of the reference period), not a time series.
-- caution: `profession_sante` is constant (general practitioners); the territory columns mix département, région and national rows.
SELECT
    "annee",
    "date",
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "effectif_medecin_install_zsd",
    "taux_evolution_annuel",
    "taux_evolution_annuel_integer"
FROM "cnam-medgen-zones-sous-dotees-infra-annuelle"
