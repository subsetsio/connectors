-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "average_daily_passenger_journeys",
    "average_journey_distances"
FROM "sg-data-d-d6921f812624c2b1bb1d68269354dc71"
