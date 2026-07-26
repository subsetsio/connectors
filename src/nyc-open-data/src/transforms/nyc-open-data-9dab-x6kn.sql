-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "srcincidentid",
    "lockinid",
    "facility",
    "lockinha",
    "lockin_hatype",
    "lockintype",
    "lockinreason",
    "lockincategory",
    "lockin_start_dttm",
    "lockin_end_dttm",
    "lock_in_duration",
    "inmatecount"
FROM "nyc-open-data-9dab-x6kn"
