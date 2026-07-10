-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The period column is a multi-year reporting interval, not a point year; do not compare it directly with annual tables without accounting for interval length.
SELECT
    "iso",
    "country",
    "desk_study",
    "period",
    "reforestation_ha_per_year",
    "forest_expansion_ha_per_year",
    "deforestation_ha_per_year"
FROM "global-forest-watch-fao-forest-change"
