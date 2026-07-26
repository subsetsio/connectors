-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "cartodb_id",
    "shape_area",
    "area_name",
    "comm_orgs",
    "epic_link",
    "ecs_link",
    "contacts"
FROM "nyc-open-data-bztk-4g6r"
