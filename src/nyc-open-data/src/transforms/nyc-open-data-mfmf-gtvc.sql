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
    "alluservolume",
    "cyclists_all",
    "cyc_greenway_only",
    "cyc_helmet_greenwy",
    "citibike_all",
    "non_citibikecyc",
    "rllrbld_scootr",
    "jogger",
    "walker",
    "cycmalehel_greenwy",
    "cycmale_greenwy",
    "cycfemalehell_greenwy",
    "cycfemale_greenwy",
    "cyclists_male",
    "cyclists_female"
FROM "nyc-open-data-mfmf-gtvc"
