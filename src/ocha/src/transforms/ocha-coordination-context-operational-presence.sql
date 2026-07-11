-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe organization presence by sector and location; filter admin_level, sector_code, and organization fields before counting organizations.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    "resource_hdx_id",
    "org_acronym",
    "org_name",
    "sector_code",
    "sector_name",
    "reference_period_start",
    "reference_period_end",
    "org_type_code",
    "org_type_description"
FROM "ocha-coordination-context-operational-presence"
