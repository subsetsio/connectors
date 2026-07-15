-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ave_daily_traffic_volume_entering_city"
FROM "sg-data-d-3136f317a1f282a33fe7a2f6a907c047"
