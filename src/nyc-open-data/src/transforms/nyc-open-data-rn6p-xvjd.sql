-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inspection_no",
    "inspection_date",
    "violations",
    "warnings"
FROM "nyc-open-data-rn6p-xvjd"
