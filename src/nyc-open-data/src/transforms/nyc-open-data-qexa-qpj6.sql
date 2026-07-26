-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "borough",
    "lp_number",
    "most_current",
    "lm_name",
    "site_status",
    "last_action",
    "public_hearing",
    "desig_date",
    "calen_date",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-qexa-qpj6"
