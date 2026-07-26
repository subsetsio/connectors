-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "ntaname",
    "sitename",
    "siteaddr",
    "hosted_by",
    "open_month",
    "day_hours",
    "notes",
    "website",
    "borocd",
    "councildis",
    "ct2010",
    "bbl",
    "bin",
    "latitude",
    "longitude",
    "policeprec",
    "object_id",
    "location_point",
    "app_android",
    "app_ios",
    "assembly_district",
    "congress_district",
    "dsny_district",
    "dsny_section",
    "dsny_zone",
    "senate_district"
FROM "nyc-open-data-if26-z6xq"
