-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `taux_adhesion` (OPTAM adhesion share) and `taux_evolution_annuel` are percentages and must never be summed; only `effectif_medecin_optam` is a count.
-- caution: The territory columns mix département, région and national rows.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "effectif_medecin_optam",
    "taux_evolution_annuel",
    "taux_adhesion",
    "taux_evolution_annuel_integer",
    "taux_adhesion_integer"
FROM "cnam-medecins-optam-annuelle"
