-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH" AS BIGINT) AS month,
    CAST("QUARTER" AS BIGINT) AS quarter,
    CAST("AIRLINE_ID" AS BIGINT) AS airline_id,
    "UNIQUE_CARRIER" AS unique_carrier,
    "UNIQUE_CARRIER_NAME" AS unique_carrier_name,
    "UNIQUE_CARRIER_ENTITY" AS unique_carrier_entity,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    CAST("CARRIER_GROUP" AS BIGINT) AS carrier_group,
    CAST("K110_REV_PAX_ENPLANED" AS DOUBLE) AS k110_rev_pax_enplaned,
    CAST("V110_REV_PAX_ENPLANED" AS DOUBLE) AS v110_rev_pax_enplaned,
    CAST("Z140_REV_PAX_MILES" AS DOUBLE) AS z140_rev_pax_miles,
    CAST("Z320_AVAIL_SEAT_MILES" AS DOUBLE) AS z320_avail_seat_miles,
    CAST("Z510_RAD_PERFORMED" AS DOUBLE) AS z510_rad_performed,
    CAST("Z520_RAD_SCHEDULED" AS DOUBLE) AS z520_rad_scheduled,
    "DATA_SOURCE" AS data_source,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-gde"
