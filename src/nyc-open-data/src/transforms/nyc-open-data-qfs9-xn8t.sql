-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "locationid",
    "locationtype",
    "typeoftime",
    "_location" AS location,
    "location_lat",
    "location_long",
    "_year" AS year,
    "totalusers",
    "noncyc_otheruser",
    "cyclistvolume",
    "cycbikelane",
    "cycadjacentlane",
    "cyclotherlane",
    "cyccounterflowinlane",
    "cycsidewalk",
    "cyccnterflowoutoflane",
    "femalecyc_total",
    "malecyc_total",
    "female_cyc_helmet",
    "male_cyc_helmet",
    "cycl_helmet_all",
    "cyc_under16",
    "citibike_male",
    "citibike_female",
    "citibike_all",
    "non_citibikecyc"
FROM "nyc-open-data-qfs9-xn8t"
