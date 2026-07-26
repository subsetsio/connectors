-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "doc_employee_id",
    "leave_status_desc",
    "rank_title",
    "gender"
FROM "nyc-open-data-eddp-3v5g"
