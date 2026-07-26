-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "camis",
    "dba",
    "boro",
    "building",
    "street",
    "zipcode",
    "phone",
    "cuisine_description",
    "inspection_date",
    "_action" AS action,
    "violation_code",
    "violation_description",
    "critical_flag",
    "score",
    "grade",
    "grade_date",
    "record_date",
    "inspection_type",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "_location" AS location
FROM "nyc-open-data-43nn-pn8j"
