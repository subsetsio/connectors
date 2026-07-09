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
    "total_pax_lp",
    "total_pax_pc",
    "term_pax_tp",
    "term_pax_lp",
    "term_pax_pc",
    "tran_pax_tp",
    "tran_pax_lp",
    "tran_pax_pc",
    "release_period",
    "family"
FROM "civil-aviation-authority-airport-09"
