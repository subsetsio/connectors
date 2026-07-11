-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The value column carries many different primary-dealer measures; filter by keyid or description before aggregating values.
SELECT
    "asofdate",
    "keyid",
    "value",
    "seriesbreak",
    "description"
FROM "ny-fed-primary-dealer-values"
