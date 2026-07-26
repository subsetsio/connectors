-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "arrest_key",
    "arrest_date",
    "pd_cd",
    "pd_desc",
    "ky_cd",
    "ofns_desc",
    "law_code",
    "law_cat_cd",
    "arrest_boro",
    "arrest_precinct",
    "jurisdiction_code",
    "age_group",
    "perp_sex",
    "perp_race",
    "x_coord_cd",
    "y_coord_cd",
    "latitude",
    "longitude",
    "_location" AS location
FROM "nyc-open-data-uip8-fykc"
