-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "districtcode",
    "mgp_curb_pri",
    "mgp_curb_sec",
    "mgp_ezp_pri",
    "mgp_ezp_sec",
    "mgp_roro37_pri",
    "mgp_roro37_sec",
    "mgp_roro_pri",
    "mgp_roro_sec",
    "org_bask",
    "org_curb_pri",
    "org_curb_sec",
    "org_doe",
    "org_gm_sat",
    "org_gm_sun",
    "pap_curb_pri",
    "pap_curb_sec",
    "pap_ezp_pri",
    "pap_ezp_sec",
    "pap_roro_pri",
    "pap_roro_sec",
    "ref_curb_pri",
    "ref_curb_sec",
    "ref_ezp_pri",
    "ref_ezp_sec",
    "ref_roro_pri",
    "ref_roro_sec",
    "shape_area",
    "shape_length",
    "multipolygon",
    "objectid"
FROM "nyc-open-data-fpv2-r9br"
