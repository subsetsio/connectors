-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "existing_site_identified",
    "proposed_leased_facility",
    "district",
    "project",
    "school",
    "boro",
    "forecast_capacity",
    "design_start",
    "constr_start",
    "actual_est_compl",
    "total_est_cost",
    "previousappropriations",
    "funding_reqd_fy_2529",
    "needed_tocomplete"
FROM "nyc-open-data-kydh-ijhc"
