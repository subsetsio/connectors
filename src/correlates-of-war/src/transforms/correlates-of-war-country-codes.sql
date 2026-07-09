-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw source includes duplicate full country-code rows for some historical states, so this reference table is published without a declared key.
SELECT
    "StateAbb" AS stateabb,
    "CCode" AS ccode,
    "StateNme" AS statenme
FROM "correlates-of-war-country-codes"
