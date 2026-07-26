-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sited",
    "leased",
    "district",
    "project",
    "school",
    "boro",
    "forecast_capacity",
    "design_start",
    "construction_start",
    "actual_est_comp",
    "total_est_comp",
    "previous_appropriations",
    "funding_reqd_fy_2024",
    "needed_to_complete"
FROM "nyc-open-data-xs6e-ka4w"
