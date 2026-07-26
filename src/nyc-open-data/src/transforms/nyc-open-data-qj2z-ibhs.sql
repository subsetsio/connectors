-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "dataset_name",
    "dataset_description",
    "update_frequency",
    "original_plan_date",
    "latest_plan_date",
    "release_status",
    "release_date",
    "url",
    "u_id",
    "agency_notes",
    "from_the_latest_open_data_plan"
FROM "nyc-open-data-qj2z-ibhs"
