-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_dbn",
    "date",
    "enrolled",
    "absent",
    "present",
    "released"
FROM "nyc-open-data-x3bb-kg5j"
