-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "borough",
    "block",
    "lot",
    "desig_address",
    "bbl",
    "lm_name",
    "lp_number",
    "site_desc",
    "site_status",
    "lm_name2",
    "desig_date",
    "lm_type",
    "report_url",
    "cd",
    "council",
    "latitude",
    "longitude",
    "bct2020",
    "nta2020",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-buis-pvji"
