-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "version",
    "establishment_type_group",
    "breakdown_topic",
    "breakdown",
    CAST("school_count" AS BIGINT) AS school_count,
    CAST("pupil_count" AS BIGINT) AS pupil_count,
    CAST("attainment8_sum" AS DOUBLE) AS attainment8_sum,
    CAST("attainment8_average" AS DOUBLE) AS attainment8_average,
    CAST("engmath_entering_total" AS BIGINT) AS engmath_entering_total,
    CAST("engmath_entering_percent" AS DOUBLE) AS engmath_entering_percent,
    CAST("engmath_95_total" AS BIGINT) AS engmath_95_total,
    CAST("engmath_95_percent" AS DOUBLE) AS engmath_95_percent,
    CAST("engmath_94_total" AS BIGINT) AS engmath_94_total,
    CAST("engmath_94_percent" AS DOUBLE) AS engmath_94_percent,
    CAST("ebacc_entering_total" AS BIGINT) AS ebacc_entering_total,
    CAST("ebacc_entering_percent" AS DOUBLE) AS ebacc_entering_percent,
    CAST("ebacc_95_total" AS BIGINT) AS ebacc_95_total,
    CAST("ebacc_95_percent" AS DOUBLE) AS ebacc_95_percent,
    CAST("ebacc_94_total" AS BIGINT) AS ebacc_94_total,
    CAST("ebacc_94_percent" AS DOUBLE) AS ebacc_94_percent,
    CAST("ebacc_aps_sum" AS DOUBLE) AS ebacc_aps_sum,
    CAST("ebacc_aps_average" AS DOUBLE) AS ebacc_aps_average,
    "progress8_pupil_count",
    "progress8_sum",
    "progress8_average",
    "progress8_lower_95_ci",
    "progress8_upper_95_ci"
FROM "dfe-19e39901-560d-f972-b6f3-dd085539c095"
