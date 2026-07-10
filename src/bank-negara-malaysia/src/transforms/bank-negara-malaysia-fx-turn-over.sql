-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw feed can repeat an observation date; use the published transform for one row per date.
SELECT
    "date",
    "total_sum"
FROM "bank-negara-malaysia-fx-turn-over"
WHERE "date" IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY "date" ORDER BY "date") = 1
