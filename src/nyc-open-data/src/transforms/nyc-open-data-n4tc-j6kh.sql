-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_code",
    "borough_name",
    "dob",
    "inspection_category",
    "inspection_date",
    "date_requested",
    "request_status_description"
FROM "nyc-open-data-n4tc-j6kh"
