-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows combine staffing measures with directory fields; contact fields are descriptive metadata, not measures.
SELECT
    "report_year",
    "entity_cd",
    "school_name",
    "year",
    "district_cd",
    "district_name",
    "cso_name",
    "street",
    "city",
    CAST("phone" AS BIGINT) AS phone,
    "grade_range",
    "num_princ",
    "num_teach",
    "num_counselors",
    "num_social",
    "per_attend",
    "per_turn_all",
    "per_turn_five_yrs"
FROM "new-york-state-education-department-studed-staff"
