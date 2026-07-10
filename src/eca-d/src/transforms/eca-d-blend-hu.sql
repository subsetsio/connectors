-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `source_id` is part of row identity: a station and date can have multiple underlying source series, so do not aggregate by station/date without deciding how to handle source series.
SELECT
    "station_id",
    "source_id",
    "date",
    CAST("value" AS DOUBLE) AS "value",
    "quality"
FROM "eca-d-blend-hu"
