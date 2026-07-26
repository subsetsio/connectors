-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bin",
    "bbl",
    "borough",
    "block",
    "lot",
    "lp_number",
    "lm_name",
    "pluto_address",
    "desig_address",
    "public_hearing",
    "lm_type",
    "hist_district",
    "other_hearings",
    "boundaries",
    "most_current",
    "site_status",
    "last_action",
    "count_bldg",
    "non_bldg",
    "vacant_lot",
    "secnd_bldg",
    "desig_date",
    "calen_date",
    "latitude",
    "longitude",
    "council",
    "cd",
    "bct2020",
    "nta2020",
    "_location" AS location
FROM "nyc-open-data-ncre-qhxs"
