-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Every dimension carries an aggregate member: `cla_age_5`/`sexe` include all-ages and both-sexes codes, and `region`/`dept` include national and régional aggregates. Summing `ntop` or `npop` without filtering each dimension to its detail members multiply-counts patients.
-- caution: `top` spans several levels of the pathology hierarchy; a patient with several pathologies is counted under each, so pathology totals do not add up to the population.
-- caution: `prev` is a prevalence rate (share of `npop`) and must never be summed.
SELECT
    "annee",
    "patho_niv1",
    "patho_niv2",
    "patho_niv3",
    "top",
    "cla_age_5",
    CAST("sexe" AS BIGINT) AS sexe,
    "region",
    "dept",
    "ntop",
    "npop",
    "prev",
    "niveau_prioritaire",
    "libelle_classe_age",
    "libelle_sexe",
    "tri"
FROM "cnam-effectifs"
