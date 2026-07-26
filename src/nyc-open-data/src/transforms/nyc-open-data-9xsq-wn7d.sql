-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "_name" AS name,
    "bin",
    "doitt_id",
    "base_bbl",
    "objectid",
    "construction_year",
    "demolition_year",
    "feature_code",
    "geom_source",
    "ground_elevation",
    "height_roof",
    "last_edited_date",
    "last_status_type",
    "map_pluto_bbl"
FROM "nyc-open-data-9xsq-wn7d"
