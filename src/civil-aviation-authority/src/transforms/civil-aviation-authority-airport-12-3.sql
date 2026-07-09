-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Route analysis tables contain directional airport-pair dimensions and should not be summed without choosing the intended route and reporting-airport level.
SELECT
    "rundate",
    "this_period",
    "last_period",
    "grp_cd",
    "grp_name",
    "apt1_apt_name",
    "apt2_apt_name",
    "total_pax_tp",
    "total_pax_shd_tp",
    "total_pax_cht_tp",
    "total_pax_lp",
    "total_pax_shd_lp",
    "total_pax_cht_lp",
    "total_pax_pc",
    "release_period",
    "family"
FROM "civil-aviation-authority-airport-12-3"
