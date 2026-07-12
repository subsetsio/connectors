-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Photos are media metadata linked to observations; joining photos to observations can duplicate observation rows when an observation has multiple photos.
-- caution: The source includes photo_uuid as the media record identifier, but this factory model publishes the large photo snapshot as keyless because exact uniqueness verification is impractical in the local model profiler.
SELECT
    "photo_uuid",
    CAST("photo_id" AS BIGINT) AS "photo_id",
    "observation_uuid",
    CAST("observer_id" AS BIGINT) AS "observer_id",
    "extension",
    "license",
    CAST("width" AS BIGINT) AS "width",
    CAST("height" AS BIGINT) AS "height",
    CAST("position" AS BIGINT) AS "position"
FROM "inaturalist-photos"
