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
    "x_coord_cd",
    "y_coord_cd",
    "latitude",
    "longitude"
FROM "nyc-open-data-5ucz-vwe8"
