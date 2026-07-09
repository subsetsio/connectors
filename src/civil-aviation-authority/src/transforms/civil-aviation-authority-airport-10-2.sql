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
    "total_pax_shd_tp",
    "total_pax_cht_tp",
    "total_pax_tp",
    "total_pax_lp",
    "total_pax_pc",
    "release_period",
    "family"
FROM "civil-aviation-authority-airport-10-2"
