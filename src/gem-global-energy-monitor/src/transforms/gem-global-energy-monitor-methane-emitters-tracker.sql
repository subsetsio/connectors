-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gem_project_id",
    "pipeline_name",
    "gem_wiki",
    "status",
    "length_merged_km",
    "capacitybcm_y",
    "emissions_factor_2019_tonnes_kilometer",
    "emissions_if_operational_tonnes_yr",
    "emissions_if_operational_lower_bound_tonnes_yr",
    "emissions_if_operational_upper_bound_tonnes_yr",
    "countries_areas",
    "wktformat"
FROM "gem-global-energy-monitor-methane-emitters-tracker"
