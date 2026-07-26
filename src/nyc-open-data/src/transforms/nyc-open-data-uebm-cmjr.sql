-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_name" AS name,
    "boro",
    "cb",
    "on_street",
    "crossstreet_1",
    "crossstreet_2",
    "area_sf",
    "area_acres",
    "project_type"
FROM "nyc-open-data-uebm-cmjr"
