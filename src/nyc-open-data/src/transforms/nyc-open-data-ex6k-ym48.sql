-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year_fy",
    "claim",
    "borough",
    "occurrence_date",
    "filed_date",
    "claim_type",
    "disposition_date",
    "disposition_amount",
    "agency",
    "claim_action"
FROM "nyc-open-data-ex6k-ym48"
