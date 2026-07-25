-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    CAST("drivers_male" AS BIGINT) AS drivers_male,
    CAST("drivers_male_1" AS DOUBLE) AS drivers_male_1,
    CAST("drivers_female" AS BIGINT) AS drivers_female,
    CAST("drivers_female_1" AS DOUBLE) AS drivers_female_1,
    CAST("drivers_total" AS BIGINT) AS drivers_total,
    CAST("drivers_per_vehicles" AS DOUBLE) AS drivers_per_vehicles,
    CAST("residents" AS BIGINT) AS residents,
    CAST("residents_male16" AS BIGINT) AS residents_male16,
    CAST("residents_female16" AS BIGINT) AS residents_female16,
    CAST("residents_16" AS BIGINT) AS residents_16,
    CAST("drivers_per_1000residents" AS BIGINT) AS drivers_per_1000residents,
    CAST("drivers_per_1000residents16" AS BIGINT) AS drivers_per_1000residents16
FROM "u-s-department-of-transportation-a6pv-7q2j"
