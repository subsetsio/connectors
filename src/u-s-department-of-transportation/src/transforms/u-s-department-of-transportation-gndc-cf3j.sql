-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "zone_name",
    CAST("link_id" AS BIGINT) AS link_id,
    "segmentid"
FROM "u-s-department-of-transportation-gndc-cf3j"
