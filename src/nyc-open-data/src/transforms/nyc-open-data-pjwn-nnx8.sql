-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_dbn",
    "school_name",
    "is_ctedesignated_high_school",
    "cte_program_name",
    "cte_program_industry_cluster",
    "number_of_industry_partners",
    "nysed_approval_status",
    "enrolled_student_grades",
    "cte_enrolled_student_count"
FROM "nyc-open-data-pjwn-nnx8"
