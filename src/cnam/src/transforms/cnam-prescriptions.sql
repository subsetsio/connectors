-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `poste_prescription` carries an all-posts aggregate alongside the individual prescription posts, and aggregate members also exist in `profession_sante` and the territory columns — filter each before summing `montant_total_prescription`.
-- caution: `montant_moyen_prescription` is a per-practitioner mean and is never summable.
SELECT
    "annee",
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "poste_prescription",
    "libelle_poste_prescription",
    "montant_total_prescription",
    "montant_moyen_prescription",
    "vision_generale_all",
    "vision_generale_prescriptions",
    "vision_profession_territoire",
    "montant_total_prescription_integer",
    "montant_moyen_prescription_integer"
FROM "cnam-prescriptions"
