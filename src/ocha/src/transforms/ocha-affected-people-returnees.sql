-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are directional origin-to-asylum returnee observations; do not aggregate origin and asylum dimensions as if they were a single location.
SELECT
    "resource_hdx_id",
    "population_group",
    "gender",
    "age_range",
    "min_age",
    "max_age",
    "population",
    "reference_period_start",
    "reference_period_end",
    "origin_location_code",
    "origin_location_name",
    "asylum_location_code",
    "asylum_location_name"
FROM "ocha-affected-people-returnees"
