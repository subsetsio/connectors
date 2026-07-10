-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Event" AS event,
    CAST("Year" AS BIGINT) AS year,
    "Character" AS character,
    "Value" AS value,
    "Rate" AS rate,
    "Type" AS type,
    "Count" AS count
FROM "cdc-jkcx-ndu8"
