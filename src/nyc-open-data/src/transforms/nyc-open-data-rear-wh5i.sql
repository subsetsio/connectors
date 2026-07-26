-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "location_name",
    "location_code",
    "borough",
    "geographical_district_code",
    "register",
    "building_name",
    "schools",
    "nypd_site_code",
    "nypd_site_name",
    "schools_in_building",
    "major_n",
    "oth_n",
    "nocrim_n",
    "prop_n",
    "vio_n",
    "engroupa",
    "rangea",
    "avgofmajor_n",
    "avgofoth_n",
    "avgofnocrim_n",
    "avgofprop_n",
    "avgofvio_n",
    "geocode",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-rear-wh5i"
