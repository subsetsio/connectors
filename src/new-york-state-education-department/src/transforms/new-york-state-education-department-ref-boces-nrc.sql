-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference rows are year-versioned crosswalk records for geography and Need/Resource-Capacity classifications.
SELECT
    "report_year",
    "entity_cd",
    "school_name",
    "year",
    "district_cd",
    "district_name",
    "boces_cd",
    "boces_name",
    "county_cd",
    "county_name",
    CAST("needs_index" AS BIGINT) AS needs_index,
    "needs_index_description",
    CAST("institution_id" AS BIGINT) AS institution_id
FROM "new-york-state-education-department-ref-boces-nrc"
