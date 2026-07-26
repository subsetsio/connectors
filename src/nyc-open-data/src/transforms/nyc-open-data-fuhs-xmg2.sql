-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_and_time_of_initial_call",
    "date_and_time_of_ranger_response",
    "borough",
    "property",
    "_location" AS location,
    "species_description",
    "call_source",
    "species_status",
    "animal_condition",
    "duration_of_response",
    "age",
    "animal_class",
    "_311sr_number" AS 311sr_number,
    "final_ranger_action",
    "of_animals",
    "pep_response",
    "animal_monitored",
    "rehabilitator",
    "hours_spent_monitoring",
    "police_response",
    "esu_response",
    "acc_intake_number"
FROM "nyc-open-data-fuhs-xmg2"
