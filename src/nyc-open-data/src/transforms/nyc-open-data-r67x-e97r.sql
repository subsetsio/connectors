-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inquiry_id",
    "inquiry_type",
    "assigned_agency",
    "inquiry",
    "dataset_name",
    "dataset_url",
    "assigned_agencys_response",
    "status",
    "date_submitted",
    "data_as_of"
FROM "nyc-open-data-r67x-e97r"
