-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `profession_sante` is constant (general practitioners). The territory columns mix département, région and national rows; `taux_evolution_annuel` is a percentage change.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "effectif_primo_installe",
    "taux_evolution_annuel",
    "taux_evolution_annuel_integer"
FROM "cnam-primo-installes-medgen-annuelle"
