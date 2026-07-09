-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "report_period",
    "airport_cluster",
    "rpt_apt_grp_cd",
    "rpt_apt_grp_name",
    "rpt_apt_name",
    "total_pax",
    "pax_term_shd_uk",
    "pax_tran_shd_uk",
    "pax_term_shd_fe",
    "pax_tran_shd_fe",
    "pax_term_shd_fn",
    "pax_tran_shd_fn",
    "pax_term_cht_uk",
    "pax_tran_cht_uk",
    "pax_term_cht_fe",
    "pax_tran_cht_fe",
    "pax_term_cht_fn",
    "pax_tran_cht_fn",
    "release_period",
    "family",
    "pax_term_shd_eu",
    "pax_tran_shd_eu",
    "pax_term_cht_eu",
    "pax_tran_cht_eu"
FROM "civil-aviation-authority-airport-08"
