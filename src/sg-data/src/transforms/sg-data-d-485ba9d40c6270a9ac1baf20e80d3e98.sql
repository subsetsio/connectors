-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "school_type",
    "student_sec"
FROM "sg-data-d-485ba9d40c6270a9ac1baf20e80d3e98"
