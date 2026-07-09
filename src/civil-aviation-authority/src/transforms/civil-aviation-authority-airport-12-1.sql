-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Route analysis tables contain directional airport-pair dimensions and should not be summed without choosing the intended route and reporting-airport level.
SELECT
    "rundate",
    "report_period",
    "region_num",
    "foreign_region",
    "foreign_country",
    "uk_group",
    "uk_apt",
    "foreign_apt",
    "ty_t_pax",
    "ty_s_pax",
    "ty_c_pax",
    "ly_t_pax",
    "ly_s_pax",
    "ly_c_pax",
    "pc_change",
    "release_period",
    "family"
FROM "civil-aviation-authority-airport-12-1"
