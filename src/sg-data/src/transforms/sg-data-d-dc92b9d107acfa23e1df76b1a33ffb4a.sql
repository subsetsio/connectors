-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "school",
    "sex",
    "student_enrolment",
    "no_of_teacher",
    "no_of_vice_principal",
    "no_of_principal",
    "no_of_education_partners"
FROM "sg-data-d-dc92b9d107acfa23e1df76b1a33ffb4a"
