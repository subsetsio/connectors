-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_dbn",
    "community_school_district",
    "city_council_district",
    "school_level",
    "full_time_health_teachers",
    "f_status_health_teachers",
    "itinerant_health_teachers",
    "sum_of_f_status_and_itinerant",
    "total_part_time_and_full_time_health_teachers"
FROM "nyc-open-data-qa4d-xc73"
