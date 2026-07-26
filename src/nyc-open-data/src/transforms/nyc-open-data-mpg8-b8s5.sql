-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "existing_site_identified",
    "district",
    "project",
    "school",
    "leased",
    "boro",
    "forecast_capacity",
    "design_start",
    "constr_start",
    "actual_estcompl",
    "total_estcost",
    "previousappropriations",
    "fundingreqd",
    "needed_tocomplete"
FROM "nyc-open-data-mpg8-b8s5"
