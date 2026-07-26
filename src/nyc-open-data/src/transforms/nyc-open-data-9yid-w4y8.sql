-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "construction_id",
    "full_capital",
    "requirements",
    "inhouse",
    "unknown_parks",
    "nonparks",
    "who_nonparks",
    "sign_present",
    "area_clean",
    "fenced_off",
    "_access" AS access,
    "workers_present",
    "_comments" AS comments,
    "inspection_id"
FROM "nyc-open-data-9yid-w4y8"
