-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bid",
    "_first" AS first,
    "_last" AS last,
    "title_contact_persons",
    "street",
    "suitefl",
    "city",
    "state",
    "postcode",
    "website",
    "representative_or_appointee",
    "formed",
    "dsbs_contact",
    "bp_staff",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-pvxf-9irb"
