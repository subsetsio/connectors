-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "serial_no",
    "name",
    "q1_cleaningstartdate",
    "q1_cleaningenddate",
    "remarks_q1",
    "q2_cleaningstartdate",
    "q2_cleaningenddate",
    "remarks_q2",
    "q3_cleaningstartdate",
    "q3_cleaningenddate",
    "remarks_q3",
    "q4_cleaningstartdate",
    "q4_cleaningenddate",
    "remarks_q4",
    "other_works_startdate",
    "other_works_enddate",
    "remarks_other_works",
    "latitude_hc",
    "longitude_hc",
    "photourl",
    "address_myenv",
    "no_of_market_stalls",
    "no_of_food_stalls",
    "description_myenv",
    "status",
    "google_3d_view",
    "google_for_stall"
FROM "sg-data-d-bda4baa634dd1cc7a6c7cad5f19e2d68"
