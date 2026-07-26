-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_dbn",
    "school_name",
    "program_code",
    "selection_criteria"
FROM "nyc-open-data-9gs9-zhxw"
