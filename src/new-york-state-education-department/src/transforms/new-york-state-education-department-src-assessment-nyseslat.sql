-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: NYSESLAT rows are English-language-proficiency assessment aggregates for ELL students; overlapping subgroup rows should not be summed.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "subject",
    "subgroup_name",
    "tested",
    "not_tested",
    "num_ent",
    "per_ent",
    "num_emer",
    "per_emer",
    "num_tran",
    "per_tran",
    "num_exp",
    "per_exp",
    "num_com",
    "per_com",
    "institution_id",
    "total",
    "per_ntest",
    "per_test"
FROM "new-york-state-education-department-src-assessment-nyseslat"
