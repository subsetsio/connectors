-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Suspension percentages are rates and should not be summed across institutions.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "num_suspensions",
    "per_suspensions",
    "data_reported"
FROM "new-york-state-education-department-studed-suspensions"
