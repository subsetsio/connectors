-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "oid",
    "blockcode",
    "geo_id",
    "bctcb2010",
    "borocode",
    "nta_code",
    "nta_name",
    "borough",
    "puma",
    "maximum_residential_broadband_speed_by_block",
    "residential_isp_count_by_block",
    "commerical_fiber_count_by_block"
FROM "nyc-open-data-8ess-ssnw"
