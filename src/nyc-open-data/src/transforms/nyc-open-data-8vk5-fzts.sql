-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "process",
    "dbn",
    "school_name",
    "program_code",
    "program_name",
    "admissions_method_for_students_entering_in_fall_2020",
    "diversity_in_admissions_priority_for_students_entering_in_fall_2020",
    "selection_criteria_for_students_entering_in_fall_2020"
FROM "nyc-open-data-8vk5-fzts"
