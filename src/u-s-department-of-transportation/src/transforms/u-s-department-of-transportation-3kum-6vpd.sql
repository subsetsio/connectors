-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "ntd_id",
    "reporter_name",
    "reporter_type_desc_short",
    "mode_code",
    "service_type_code",
    "place_geo_id",
    "place_name",
    "geo_service_level_desc",
    "county_geo_id",
    "county_name",
    "county_state_name"
FROM "u-s-department-of-transportation-3kum-6vpd"
