-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "facility",
    "nonproduction_court",
    "nonproduction_visits",
    "nonproduction_refusal",
    "nonproduction_walkout",
    "nonproduction_programming",
    "nonproduction_barbershop",
    "nonproduction_recreation",
    "nonproduction_other",
    "total_scheduled"
FROM "nyc-open-data-5n4h-km5r"
