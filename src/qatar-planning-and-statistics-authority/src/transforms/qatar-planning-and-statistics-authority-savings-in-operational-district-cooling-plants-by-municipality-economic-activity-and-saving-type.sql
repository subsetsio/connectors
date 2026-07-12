-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nw_ltwfyr",
    "type_of_saving",
    "lbldy",
    "municipality",
    "lnsht_lqtsdy",
    "economic_activity",
    "unit",
    "value",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-savings-in-operational-district-cooling-plants-by-municipality-economic-activity-and-saving-type"
