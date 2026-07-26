-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acct_id",
    "alpha",
    "acct_num",
    "owner_name",
    "last_visit_dt",
    "last_full_insp_dt",
    "last_insp_stat",
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
FROM "nyc-open-data-ssq6-fkht"
