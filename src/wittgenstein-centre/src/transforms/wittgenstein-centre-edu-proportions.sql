-- caution: Educational attainment proportions cover ages 15-34.
WITH long AS (
    UNPIVOT "wittgenstein-centre-edu-proportions"
    ON SSP1, SSP2, SSP2mig0, SSP2mig2x, SSP3, SSP4, SSP5
    INTO NAME scenario VALUE value
)
SELECT
    region,
    region_name,
    CAST(Time AS INTEGER) AS year,
    sex,
    edu,
    edu_label,
    CAST(agest AS INTEGER) AS age_start,
    scenario,
    CAST(value AS DOUBLE) AS proportion
FROM long
WHERE value IS NOT NULL
