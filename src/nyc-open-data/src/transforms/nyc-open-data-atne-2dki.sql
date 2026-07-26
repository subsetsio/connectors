-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "program_name",
    "docket_id",
    "intake_max_severity",
    "gender",
    "program_entry_date",
    "supervision_level"
FROM "nyc-open-data-atne-2dki"
