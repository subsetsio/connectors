-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sam_number",
    "sam_name_and_link",
    "subcategory",
    "amount"
FROM "nyc-open-data-99gz-6gpw"
