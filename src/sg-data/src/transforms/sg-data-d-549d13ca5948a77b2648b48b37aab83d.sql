-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "school",
    "course_name",
    "course_code",
    "elr2b2_type",
    "elr2b2",
    "planned_intake",
    "reference"
FROM "sg-data-d-549d13ca5948a77b2648b48b37aab83d"
