-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    "MANUFACTURE_YEAR" AS manufacture_year,
    "UNIQUE_CARRIER_NAME" AS unique_carrier_name,
    "SERIAL_NUMBER" AS serial_number,
    "TAIL_NUMBER" AS tail_number,
    "AIRCRAFT_STATUS" AS aircraft_status,
    "OPERATING_STATUS" AS operating_status,
    "NUMBER_OF_SEATS" AS number_of_seats,
    "MANUFACTURER" AS manufacturer,
    "AIRCRAFT_TYPE" AS aircraft_type,
    "MODEL" AS model,
    "CAPACITY_IN_POUNDS" AS capacity_in_pounds,
    "ACQUISITION_DATE" AS acquisition_date,
    "AIRLINE_ID" AS airline_id,
    "UNIQUE_CARRIER" AS unique_carrier,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-geh"
