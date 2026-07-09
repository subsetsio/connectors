-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Census 2021 CMD tables include category totals alongside detailed categories; filter category dimensions before summing across rows.
SELECT
    "lower_tier_local_authorities_code",
    "lower_tier_local_authorities",
    CAST("household_reference_person_previously_served_in_uk_armed_forces_5_categories_code" AS BIGINT) AS household_reference_person_previously_served_in_uk_armed_forces_5_categories_code,
    "household_reference_person_previously_served_in_uk_armed_forces_5_categories",
    "value"
FROM "ons-ts074"
