-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "gradespan",
    "school_type",
    "accessibility",
    "gt_in_kindergarten",
    "nonzoned_offers",
    "dual_language_programs",
    "phone_number",
    "address",
    "x_coordinate",
    "y_coordinate",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-urzf-q2g5"
