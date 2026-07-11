-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Urban social disorder records are event-level observations; city and country fields are denormalized location attributes.
SELECT
    "eventid",
    "city_id",
    "city",
    "country",
    "iso3",
    "gwno",
    "country_hist",
    "gwno_hist",
    "region",
    "long",
    "lat",
    "ptype",
    "bday",
    "bmonth",
    "byear",
    "eday",
    "emonth",
    "eyear",
    "actor1",
    "actor2",
    "actor3",
    "target1",
    "target2",
    "npart",
    "ndeath",
    "elocal",
    "reportid1",
    "reportid2",
    "reportid3",
    "summary"
FROM "prio-6"
