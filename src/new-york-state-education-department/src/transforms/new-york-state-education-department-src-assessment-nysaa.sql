-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: NYSAA rows are alternate-assessment aggregates; interpret subject and subgroup dimensions before comparing counts.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "subject",
    "subgroup_name",
    "tested",
    "not_tested",
    "level1_count",
    "level1_pertested",
    "level2_count",
    "level2_pertested",
    "level3_count",
    "level3_pertested",
    "level4_count",
    "level4_pertested",
    "institution_id",
    "total",
    "not_tested_per",
    "exempt",
    "exempt_per",
    "per_tested",
    "level1_per",
    "level2_per",
    "level3_per",
    "level4_per",
    "proficient_count",
    "proficient_per"
FROM "new-york-state-education-department-src-assessment-nysaa"
