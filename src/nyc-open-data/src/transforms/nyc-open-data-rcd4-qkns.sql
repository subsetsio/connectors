-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unit",
    "group_name",
    "date",
    "program_month",
    "borough",
    "location_type",
    "location_name",
    "programtime",
    "program_name",
    "program_type",
    "category",
    "classification",
    "duration_of_program",
    "audience",
    "studentyouth_att",
    "optional_supply_categories",
    "activity",
    "length_of_activity_1",
    "length_of_activity_2",
    "total_participant_hours"
FROM "nyc-open-data-rcd4-qkns"
