-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "matter_name",
    "docketindex",
    "court_name",
    "judge",
    "app_docket",
    "app_court",
    "plaintiffspetitioners_firms",
    "defendantsrespondents_firms",
    "ld_division",
    "lit_start",
    "closed_date",
    "disposition",
    "total_disposition_amt",
    "total_city_payout_amt",
    "total_city_received_amt",
    "total_expenses",
    "lead_bbl"
FROM "nyc-open-data-pjgc-h7uv"
