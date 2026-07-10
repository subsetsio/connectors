-- GEOGLAM Crop Monitor — global synthesis crop-condition assessments.
-- Faithful long-format pass-through of the monthly ArcGIS synthesis layers:
-- one row per source polygon feature per assessment month. KEYLESS — once the
-- polygon geometry is dropped the same (month, country, region, crop) recurs
-- across distinct overlapping growing-area polygons, often with different
-- conditions; do NOT dedupe on the descriptive columns.
-- Residual curation only: YYYYMM -> month DATE, trim, blank/#N/A sentinels ->
-- NULL, unify the 'No data' case variant and the two 'Favourable' misspellings.
SELECT
    CAST(strptime("period" || '01', '%Y%m%d') AS DATE) AS month,
    NULLIF(TRIM("country"), '') AS country,
    NULLIF(TRIM("region"), '')  AS region,
    NULLIF(TRIM("crop"), '')    AS crop,
    CASE
        WHEN UPPER(TRIM("conditions")) IN ('', '#N/A', 'N/A', 'NA') THEN NULL
        WHEN UPPER(TRIM("conditions")) = 'NO DATA' THEN 'No Data'
        WHEN TRIM("conditions") IN ('Favuorable', 'Favourble') THEN 'Favourable'
        ELSE TRIM("conditions")
    END AS condition,
    NULLIF(TRIM("drivers"), '') AS drivers
FROM "geoglam-crop-monitor-crop-conditions"
