-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "Year" AS year,
    "Month" AS month,
    "Aircraft_Arrival" AS aircraft_arrival,
    "Aircraft_Departure" AS aircraft_departure,
    "Aircraft_Total" AS aircraft_total,
    "Passenger_Arrival" AS passenger_arrival,
    "Passenger_Departures" AS passenger_departures,
    "Passenger_Transit" AS passenger_transit,
    "Passenger_Total" AS passenger_total,
    "AirMail_Incoming" AS airmail_incoming,
    "AirMail_Outgoing" AS airmail_outgoing,
    "AirMail_Total" AS airmail_total,
    "Cargo_Total_Import" AS cargo_total_import,
    "Cargo_Total_Export" AS cargo_total_export,
    "Cargo_Total" AS cargo_total
FROM "sg-data-d-744e62bfb1c524508bce0a64a2488243"
