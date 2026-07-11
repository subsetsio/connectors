-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Annual Regents rows are subject and subgroup aggregates; filter subject and subgroup before comparing or aggregating.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "subject",
    "subgroup_name",
    "tested",
    "num_level1",
    "per_level1",
    "num_level2",
    "per_level2",
    "num_level3",
    "per_level3",
    "num_level4",
    "per_level4",
    "num_level5",
    "per_level5",
    "num_prof",
    "per_prof",
    "institution_id",
    "total_exempt",
    "num_exempt_ntest",
    "pct_exempt_ntest",
    "num_exempt_test",
    "pct_exempt_test",
    "assmnt_flag"
FROM "new-york-state-education-department-src-assessment-regents-annual"
