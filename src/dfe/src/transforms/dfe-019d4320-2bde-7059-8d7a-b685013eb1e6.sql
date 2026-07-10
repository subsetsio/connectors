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
    "social_care_group",
    "sen_provision",
    "ethnicity_major",
    "placement",
    "period_of_care_length",
    "version",
    "pupil_count",
    "attainment8_sum",
    "attainment8_average",
    "engmath_95_total",
    "engmath_95_percent",
    "engmath_94_total",
    "engmath_94_percent",
    "ebacc_entering_total",
    "ebacc_entering_percent",
    "ebacc_95_total",
    "ebacc_95_percent",
    "ebacc_94_total",
    "ebacc_94_percent",
    "ebacc_aps_sum",
    "ebacc_aps_average",
    "progress8_pupil_count",
    "progress8_sum",
    "progress8_average",
    "progress8_lower_95_ci",
    "progress8_upper_95_ci"
FROM "dfe-019d4320-2bde-7059-8d7a-b685013eb1e6"
