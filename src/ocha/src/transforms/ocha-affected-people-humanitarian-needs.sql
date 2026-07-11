-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix national and subnational administrative levels; filter admin_level and location/admin columns before summing population counts.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    "resource_hdx_id",
    "sector_code",
    "category",
    "population_status",
    "population",
    "reference_period_start",
    "reference_period_end",
    "sector_name"
FROM "ocha-affected-people-humanitarian-needs"
