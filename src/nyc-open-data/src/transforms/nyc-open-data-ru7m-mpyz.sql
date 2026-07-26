-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geo_type",
    "geo_unit",
    "active_applicants",
    "applicants_served",
    "checks_issued",
    "dollars_reimbursed",
    "total_city_managed",
    "construction_started_city_managed",
    "construction_completed_city_managed",
    "total_overall_construction",
    "construction_started_overall_construction",
    "construction_completed_overall_construction"
FROM "nyc-open-data-ru7m-mpyz"
