-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vio_id",
    "acct_num",
    "acct_owner",
    "violation_num",
    "vio_law_num",
    "vio_law_desc",
    "vio_date",
    "_action" AS action,
    "prem_addr",
    "bin",
    "community_board",
    "council_district",
    "bbl",
    "latitude",
    "longitude",
    "postcode",
    "borough",
    "number",
    "street",
    "census_tract",
    "nta"
FROM "nyc-open-data-bi53-yph3"
