-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nycha_development_name",
    "provider",
    "nycha_total_households",
    "total_big_apple_connect_subscribers",
    "percent_of_enrollment",
    "borough",
    "community_board",
    "city_council_district",
    "congressional_district",
    "state_senate_district",
    "state_assembly_district",
    "reporting_date"
FROM "nyc-open-data-t4kb-prwp"
