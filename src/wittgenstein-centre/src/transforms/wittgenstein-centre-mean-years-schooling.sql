-- caution: Mean years of schooling is reported for age groups in the 15+ population.
WITH long AS (
    UNPIVOT "wittgenstein-centre-mean-years-schooling"
    ON SSP1, SSP2, SSP2mig0, SSP2mig2x, SSP3, SSP4, SSP5
    INTO NAME scenario VALUE value
)
SELECT
    region,
    region_name,
    CAST(Time AS INTEGER) AS year,
    sex,
    CAST(agest AS INTEGER) AS age_start,
    scenario,
    CAST(value AS DOUBLE) AS mean_years_schooling
FROM long
WHERE value IS NOT NULL
