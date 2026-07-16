-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("QUARTER" AS BIGINT) AS quarter,
    "REGION" AS region,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    "CARRIER_ENTITY" AS carrier_entity,
    CAST("SCH_DEPARTURES" AS DOUBLE) AS sch_departures,
    CAST("DEP_PERFORMED" AS DOUBLE) AS dep_performed,
    CAST("COMP_DEPARTURES" AS DOUBLE) AS comp_departures,
    CAST("AVAIL_TON_MILES" AS DOUBLE) AS avail_ton_miles,
    CAST("AVAIL_SEAT_MILES" AS DOUBLE) AS avail_seat_miles,
    CAST("REV_PAX_MILES" AS DOUBLE) AS rev_pax_miles,
    CAST("REV_TON_MILES" AS DOUBLE) AS rev_ton_miles,
    CAST("AIRCRAFT_MILES" AS DOUBLE) AS aircraft_miles,
    CAST("AIRCRAFT_HOURS" AS DOUBLE) AS aircraft_hours,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-fki"
