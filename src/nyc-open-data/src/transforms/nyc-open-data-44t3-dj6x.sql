-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "building_code",
    "dbn",
    "location_name",
    "location_code",
    "address",
    "borough",
    "geographical_district_code",
    "register",
    "building_name",
    "schools",
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
    "avgofvio_n"
FROM "nyc-open-data-44t3-dj6x"
