-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "category",
    "technology_ies_strategy_ies",
    "description",
    "current_status",
    "type_of_takeaway",
    "program_area"
FROM "u-s-department-of-transportation-s379-pwfw"
