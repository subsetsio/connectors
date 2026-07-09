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
    "total_pax_fw_tp",
    "total_pax_fw_lp",
    "total_pax_fw_pc",
    "total_pax_rw_tp",
    "total_pax_rw_lp",
    "total_pax_rw_pc",
    "total_atms_fw_tp",
    "total_atms_fw_lp",
    "total_atms_fw_pc",
    "total_atms_rw_tp",
    "total_atms_rw_lp",
    "total_atms_rw_pc",
    "release_period",
    "family"
FROM "civil-aviation-authority-airport-19"
