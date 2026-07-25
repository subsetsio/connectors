-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "county",
    "census_tract_name",
    "county_meets_definition",
    "census_tract_meets_definition",
    "hdc_census_tract_meets_definition_" AS hdc_census_tract_meets_definition
FROM "u-s-department-of-transportation-mmgn-pg9s"
