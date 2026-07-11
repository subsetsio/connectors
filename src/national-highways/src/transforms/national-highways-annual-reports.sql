-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is a monthly summary for one monitoring site; ADT and AWT columns are separate measures over different daily windows and should not be summed together.
SELECT
    CAST("site_id" AS BIGINT) AS site_id,
    "year",
    "month_num",
    "month_name",
    "adt_24hour",
    "adt_24hour_large_vehicle_pct",
    "awt_24hour",
    "awt_24hour_large_vehicle_pct",
    "adt_18hour",
    "adt_18hour_large_vehicle_pct",
    "awt_18hour",
    "awt_18hour_large_vehicle_pct",
    "adt_16hour",
    "adt_16hour_large_vehicle_pct",
    "awt_16hour",
    "awt_16hour_large_vehicle_pct",
    "adt_12hour",
    "adt_12hour_large_vehicle_pct",
    "awt_12hour",
    "awt_12hour_large_vehicle_pct"
FROM "national-highways-annual-reports"
