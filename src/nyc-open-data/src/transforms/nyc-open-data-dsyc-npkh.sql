-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "sample_location",
    "time1",
    "vocs1_ppm",
    "temp1_f",
    "humidity1",
    "observations1",
    "time2",
    "vocs2_ppm",
    "temp2_f",
    "humidity2",
    "observations2",
    "time3",
    "vocs3_ppm",
    "temp3_f",
    "humidity3",
    "observations3"
FROM "nyc-open-data-dsyc-npkh"
