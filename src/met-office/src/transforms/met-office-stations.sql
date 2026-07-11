-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "station",
    "name",
    "lat",
    "lon",
    "altitude_m",
    "start_year",
    "end_year",
    "location"
FROM "met-office-stations"
