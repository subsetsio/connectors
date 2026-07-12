-- caution: Sex ratio at birth is a region-year scenario series.
WITH long AS (
    UNPIVOT "wittgenstein-centre-sex-ratio-at-birth"
    ON SSP1, SSP2, SSP2mig0, SSP2mig2x, SSP3, SSP4, SSP5
    INTO NAME scenario VALUE value
)
SELECT
    region,
    region_name,
    CAST(Time AS INTEGER) AS year,
    scenario,
    CAST(value AS DOUBLE) AS sex_ratio_at_birth
FROM long
WHERE value IS NOT NULL
