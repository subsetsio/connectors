-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "this_period",
    "last_period",
    "airport_cluster",
    "rpt_apt_grp_cd",
    "rpt_apt_grp_name",
    "rpt_apt_name",
    "total_pax_tp",
    "total_pax_eu_shd_tp",
    "total_pax_eu_cht_tp",
    "total_pax_eu_tp",
    "total_pax_eu_lp",
    "total_pax_eu_pc",
    "total_pax_oi_shd_tp",
    "total_pax_oi_cht_tp",
    "total_pax_oi_tp",
    "total_pax_oi_lp",
    "total_pax_oi_pc",
    "release_period",
    "family",
    "Run_Date" AS run_date,
    "This_Period_1" AS this_period_1,
    "Last_Period_1" AS last_period_1
FROM "civil-aviation-authority-airport-10-1"
