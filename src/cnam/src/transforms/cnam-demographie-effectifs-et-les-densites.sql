-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Every dimension carries its own aggregate member: an all-professions `profession_sante`, national/région rows in the territory columns, an all-ages `classe_age` and a both-sexes `libelle_sexe`. Summing `effectif` without filtering each dimension to its detail members multiply-counts practitioners.
-- caution: `densite` is practitioners per 100,000 inhabitants — a ratio, never summable.
SELECT
    "annee",
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "classe_age",
    "libelle_classe_age",
    "libelle_sexe",
    "effectif",
    "densite",
    "vision_generale_all",
    "vision_generale_prescriptions",
    "vision_profession_territoire"
FROM "cnam-demographie-effectifs-et-les-densites"
