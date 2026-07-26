-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "alteration_year",
    "bbl",
    "bin",
    "borough",
    "public_restroom",
    "construction_year",
    "description",
    "doitt_id",
    "doitt_source",
    "demolition_year",
    "gispropnum",
    "ground_elevation",
    "height_roof",
    "_location" AS location,
    "maintby",
    "maintbyspec",
    "omppropid",
    "parks_district",
    "_system" AS system,
    "multipolygon",
    "recreation_center",
    "featurestatus"
FROM "nyc-open-data-n8q6-i44s"
