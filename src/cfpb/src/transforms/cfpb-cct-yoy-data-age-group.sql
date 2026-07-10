-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Borrower age groups are stored as separate year-over-year measure columns, so do not sum those columns together.
SELECT
    "month",
    strptime("date", '%Y-%m')::DATE AS date,
    "younger-than-30_yoy" AS younger_than_30_yoy,
    "30-44_yoy" AS "30_44_yoy",
    "45-64_yoy" AS "45_64_yoy",
    "65-and-older_yoy" AS "65_and_older_yoy",
    "market"
FROM "cfpb-cct-yoy-data-age-group"
