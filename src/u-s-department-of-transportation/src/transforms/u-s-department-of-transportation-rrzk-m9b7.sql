-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tmc",
    CAST("road_order" AS BIGINT) AS road_order,
    "link_ids"
FROM "u-s-department-of-transportation-rrzk-m9b7"
