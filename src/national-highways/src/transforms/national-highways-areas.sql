-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("area_id" AS BIGINT) AS area_id,
    "name",
    "description",
    "x_longitude",
    "x_latitude",
    "y_longitude",
    "y_latitude"
FROM "national-highways-areas"
