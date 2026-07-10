-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Burden" AS burden,
    "Season" AS season,
    strptime("Date", '%Y-%m-%d')::DATE AS date,
    CAST("Low" AS BIGINT) AS low,
    CAST("High" AS BIGINT) AS high
FROM "cdc-sumd-iwm8"
