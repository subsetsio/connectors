-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "title",
    "instructor",
    "guid",
    "link",
    "description",
    "registration_url",
    "registration_description",
    "parkids",
    "parknames",
    "startdate",
    "enddate",
    "starttime",
    "endtime",
    "contact_phone",
    "_location" AS location,
    "categories",
    "coordinates",
    "image",
    "pubdate"
FROM "nyc-open-data-w3wp-dpdi"
