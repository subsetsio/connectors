-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "incident_key",
    "occur_date",
    "occur_time",
    "boro",
    "loc_of_occur_desc",
    "precinct",
    "jurisdiction_code",
    "loc_classfctn_desc",
    "location_desc",
    "statistical_murder_flag",
    "perp_age_group",
    "perp_sex",
    "perp_race",
    "vic_age_group",
    "vic_sex",
    "vic_race",
    "x_coord_cd",
    "y_coord_cd",
    "latitude",
    "longitude",
    "new_georeferenced_column"
FROM "nyc-open-data-98wc-x49t"
