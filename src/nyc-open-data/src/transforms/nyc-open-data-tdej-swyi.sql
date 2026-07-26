-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_year",
    "agency_name",
    "data_set_name",
    "data_set_description",
    "update_frequency",
    "release_date",
    "reason_for_removal"
FROM "nyc-open-data-tdej-swyi"
