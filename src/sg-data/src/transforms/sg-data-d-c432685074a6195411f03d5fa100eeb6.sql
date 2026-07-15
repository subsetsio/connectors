-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "From_PostalCode" AS from_postalcode,
    "To_PostalCode" AS to_postalcode,
    "From" AS from,
    "To" AS to,
    "TimeTaken_Mins" AS timetaken_mins,
    "DistanceTravelled_KM" AS distancetravelled_km
FROM "sg-data-d-c432685074a6195411f03d5fa100eeb6"
