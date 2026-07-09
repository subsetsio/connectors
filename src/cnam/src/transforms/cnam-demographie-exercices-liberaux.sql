-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate members coexist with detail members in `profession_sante`, the territory columns and `type_exercice_liberal`. Filter each dimension before summing `effectif`.
SELECT
    "annee",
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    CAST("type_exercice_liberal" AS BIGINT) AS type_exercice_liberal,
    "libelle_type_exercice_liberal",
    "effectif",
    "vision_generale_all",
    "vision_generale_prescriptions",
    "vision_profession_territoire"
FROM "cnam-demographie-exercices-liberaux"
