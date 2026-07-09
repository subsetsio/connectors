-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Daily observations on trading days only; gaps are weekends and holidays, not missing data.
-- caution: The three columns are related by construction: `sri` (the systemic risk indicator) equals `pdd` minus `add`. All are expressed in percentage points of asset value; a LOW `sri` signals elevated systemic stress.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "add",
    "sri",
    "pdd"
FROM "cleveland-fed-systemicrisk-landing-systemicrisk"
