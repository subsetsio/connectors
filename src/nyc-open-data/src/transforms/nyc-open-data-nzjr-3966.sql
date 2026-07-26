-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "title_code",
    "title_description",
    "standard_hours",
    "assignment_level",
    "union_code",
    "union_description",
    "bargaining_unit_short_name",
    "bargaining_unit_description",
    "minimum_salary_rate",
    "maximum_salary_rate",
    "investigation_before_appointment"
FROM "nyc-open-data-nzjr-3966"
