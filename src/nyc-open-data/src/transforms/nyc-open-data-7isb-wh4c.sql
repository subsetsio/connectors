-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_type",
    "doc_type",
    "doc_type_description",
    "class_code_description",
    "party1_type",
    "party2_type",
    "party3_type"
FROM "nyc-open-data-7isb-wh4c"
