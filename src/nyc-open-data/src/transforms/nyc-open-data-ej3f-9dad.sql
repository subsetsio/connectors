-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "generating_project_id",
    "transferred_floor_area",
    "transfer_date",
    "generating_building_id",
    "transfer_building_id"
FROM "nyc-open-data-ej3f-9dad"
