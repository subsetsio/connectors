-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "dbn",
    "school_type",
    "school_name",
    "address",
    "phone",
    "grades",
    "accessibility",
    "dual_language",
    "gt_in_kindergarten",
    "x_coordinate",
    "y_coordinate",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-8532-9v5k"
