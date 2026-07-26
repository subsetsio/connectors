-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "filing_agency_case_id",
    "case_number",
    "_name" AS name,
    "_type" AS type,
    "category",
    "subcategory",
    "opened",
    "original_conference",
    "original_trial_date",
    "trial_concluded",
    "record_closed",
    "premises",
    "report_issued",
    "dispo_code",
    "agency_head_decision",
    "appeal_action_date"
FROM "nyc-open-data-y3hw-z6bm"
