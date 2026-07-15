-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Month" AS month,
    "FlightType" AS flighttype,
    "AirlineType" AS airlinetype,
    "AircraftArrival" AS aircraftarrival,
    "AircraftDeparture" AS aircraftdeparture,
    "PassengerTransit" AS passengertransit
FROM "sg-data-d-8d7c6138029eea4d7ffae4f13e3a6458"
