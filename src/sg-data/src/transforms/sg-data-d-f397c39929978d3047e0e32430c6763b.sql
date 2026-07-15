-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Parameter" AS parameter,
    "Units" AS units,
    "Average" AS average,
    "Range" AS range
FROM "sg-data-d-f397c39929978d3047e0e32430c6763b"
