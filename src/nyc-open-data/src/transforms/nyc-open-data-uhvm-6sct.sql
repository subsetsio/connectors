-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_period",
    "childparent",
    "category",
    "subcategory",
    "scr_intakes",
    "indicated_investigations",
    "unsubstantiated_investigations",
    "cares_cases",
    "acs_referral_to_prevention",
    "emergency_removals",
    "article_x_filings",
    "remands_at_initial_hearings",
    "article_x_foster_care_entries"
FROM "nyc-open-data-uhvm-6sct"
