-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference rows are year-versioned grouping assignments rather than statistical measures.
SELECT
    "report_year",
    CAST("group_code" AS BIGINT) AS group_code,
    "group_name",
    "entity_cd",
    "entity_name",
    "institution_id"
FROM "new-york-state-education-department-ref-institution-grouping"
