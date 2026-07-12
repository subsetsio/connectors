-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table contains annual local-authority traffic estimates; do not sum across local authorities without accounting for the geographic level and boundary coding used by the source.
SELECT
    CAST("local_authority_id" AS BIGINT) AS local_authority_id,
    "local_authority_name",
    "local_authority_code",
    CAST("year" AS BIGINT) AS year,
    CAST("link_length_km" AS BIGINT) AS link_length_km,
    CAST("link_length_miles" AS BIGINT) AS link_length_miles,
    CAST("cars_and_taxis" AS DOUBLE) AS cars_and_taxis,
    CAST("all_motor_vehicles" AS DOUBLE) AS all_motor_vehicles
FROM "uk-dft-gb-road-traffic-counts"
