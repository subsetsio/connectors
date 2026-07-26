-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_id",
    "project_name",
    "administering_agent",
    "project_status",
    "total_ih_floor_area",
    "transferred_ih_floor_area",
    "remaining_ih_floor_area"
FROM "nyc-open-data-jafx-rvrb"
