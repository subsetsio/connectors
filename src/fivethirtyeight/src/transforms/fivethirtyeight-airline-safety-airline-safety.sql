-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "airline",
    "avail_seat_km_per_week",
    "incidents_85_99",
    "fatal_accidents_85_99",
    "fatalities_85_99",
    "incidents_00_14",
    "fatal_accidents_00_14",
    "fatalities_00_14"
FROM "fivethirtyeight-airline-safety-airline-safety"
