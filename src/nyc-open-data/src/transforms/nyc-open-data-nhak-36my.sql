-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "school_dbn",
    "community_school_district",
    "city_council_district",
    "school_name",
    "of_teachers_assigned_to_teach_health"
FROM "nyc-open-data-nhak-36my"
