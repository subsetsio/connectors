-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Borrower credit-score levels are stored as separate year-over-year measure columns, so do not sum those columns together.
SELECT
    "month",
    strptime("date", '%Y-%m')::DATE AS date,
    "deep-subprime_yoy" AS deep_subprime_yoy,
    "subprime_yoy",
    "near-prime_yoy" AS near_prime_yoy,
    "prime_yoy",
    "super-prime_yoy" AS super_prime_yoy,
    "market"
FROM "cfpb-cct-yoy-data-score-level"
