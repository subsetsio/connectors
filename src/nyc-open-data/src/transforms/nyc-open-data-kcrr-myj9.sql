-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "shape_leng",
    "shape_area",
    "boro_code",
    "boro_name",
    "county_fip",
    "ntacode",
    "ntaname",
    "id",
    "_zone" AS zone,
    "_class" AS class,
    "zonename"
FROM "nyc-open-data-kcrr-myj9"
