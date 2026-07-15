-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "pm10_24hour_mean_99th_per"
FROM "sg-data-d-dc29ecdc06f1f2b42c3dd06dd1ab8e6b"
