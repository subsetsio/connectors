-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "generating_project_id",
    "floor_area_generated",
    "generating_building_id"
FROM "nyc-open-data-qcru-xhuq"
