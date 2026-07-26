-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "community_school_district",
    "cte_designated_high_school",
    "category",
    "n_students_enrolled_in_schools_offering_cte",
    "n_students_enrolled_in_cte",
    "students_enrolled_in_cte"
FROM "nyc-open-data-8vqd-3345"
