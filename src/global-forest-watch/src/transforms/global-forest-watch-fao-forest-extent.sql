-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "iso",
    "country",
    "desk_study",
    "year",
    "primary_ha",
    "naturally_regenerating_forest_ha",
    "planted_forest_ha",
    "forest_ha",
    "non_forest_ha",
    "total_land_area_ha"
FROM "global-forest-watch-fao-forest-extent"
