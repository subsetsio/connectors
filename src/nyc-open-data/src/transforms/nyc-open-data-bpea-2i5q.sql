-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "material_group",
    "material_category",
    "dsny_diversion_summary_category",
    "aggregate_percent",
    "refuse_percent",
    "mgp_metal_glass_plastic_percent",
    "paper_percent",
    "organics_percent",
    "generator_aggregate_residential_schools_nycha_litter_baskets",
    "residential_strata_citywide_hdhi_hdli_hdmi_ldhi_ldli_ldmi_mdhi_mdli_mdmi",
    "period_annual_season_1_season_2"
FROM "nyc-open-data-bpea-2i5q"
