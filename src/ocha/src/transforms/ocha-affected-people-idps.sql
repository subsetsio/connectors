-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix national and subnational administrative levels and assessment types; filter admin_level and assessment_type before aggregating population counts.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    "resource_hdx_id",
    "reporting_round",
    "assessment_type",
    "operation",
    "population",
    "reference_period_start",
    "reference_period_end"
FROM "ocha-affected-people-idps"
