-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "requirements",
    "opportunity_id",
    "content_id",
    "summary",
    "category_description",
    "title",
    "display_url",
    "recurrence_type",
    "street_address",
    "_2nd_address" AS 2nd_address,
    "city",
    "state",
    "postcode",
    "country",
    "website",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-shpd-5q9m"
