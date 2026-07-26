-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "evnt_key",
    "occur_date",
    "tour",
    "law_code",
    "law_desc",
    "law_type",
    "age_group",
    "sex",
    "race",
    "precinct",
    "jurisdition_code",
    "city_nm",
    "x_coord_cd",
    "y_coord_cd",
    "latitude",
    "longitude",
    "location_point"
FROM "nyc-open-data-hxbk-grd3"
