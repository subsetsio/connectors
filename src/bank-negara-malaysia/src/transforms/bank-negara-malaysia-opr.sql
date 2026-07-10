-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows record policy-rate decision dates and levels, not a daily forward-filled policy-rate calendar.
-- caution: The raw feed can repeat a decision date; use the published transform for one row per decision date.
SELECT
    "year",
    "date",
    "change_in_opr",
    "new_opr_level"
FROM "bank-negara-malaysia-opr"
WHERE "date" IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY "date" ORDER BY "date") = 1
