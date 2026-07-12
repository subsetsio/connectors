-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are voluntary citizen-science observations, not a spatially or temporally regular survey grid; aggregate by location or date only after accounting for uneven observer coverage and repeat submissions.
SELECT
    CAST("id" AS BIGINT) AS id,
    "obs_type",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("elevation_m" AS DOUBLE) AS elevation_m,
    strptime("local_date", '%Y-%m-%d')::DATE AS local_date,
    "local_time",
    strptime("ut_date", '%Y-%m-%d')::DATE AS ut_date,
    "ut_time",
    CAST("limiting_mag" AS BIGINT) AS limiting_mag,
    CAST("sqm_reading" AS DOUBLE) AS sqm_reading,
    "sqm_serial",
    "cloud_cover",
    "constellation",
    "sky_comment",
    "location_comment",
    "country",
    CAST("file_year" AS BIGINT) AS file_year
FROM "globe-at-night-observations"
