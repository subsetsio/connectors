-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Attendance rates are annual institution-level measures; average or weight rates rather than summing them.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "attendance_rate",
    "data_reported"
FROM "new-york-state-education-department-studed-attendance"
