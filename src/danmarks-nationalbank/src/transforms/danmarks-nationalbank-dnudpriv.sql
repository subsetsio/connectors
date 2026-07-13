-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Raw StatBank extract contains duplicate rows even across all emitted fields; treat rows as source observations and aggregate with care.
SELECT
    "instituttype",
    "sporg",
    "tiden",
    "time",
    "value"
FROM "danmarks-nationalbank-dnudpriv"
