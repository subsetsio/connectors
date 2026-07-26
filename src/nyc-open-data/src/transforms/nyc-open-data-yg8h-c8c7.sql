-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "cte_designated_high_school",
    "program_cip_code",
    "program_name",
    "industry_cluster",
    "number_of_industry_partners",
    "is_nysed_approved",
    "grade_levels_served",
    "enrolled_student_counts",
    "number_of_school_staff_attending_professional_development_events_held_by_cte"
FROM "nyc-open-data-yg8h-c8c7"
