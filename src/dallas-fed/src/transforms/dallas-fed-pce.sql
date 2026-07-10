-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include multiple inflation horizons for each date; filter horizon before comparing values.
SELECT
    "date",
    "horizon",
    "value"
FROM "dallas-fed-pce"
