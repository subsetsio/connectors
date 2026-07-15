-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "Day" AS day,
    "Date" AS date,
    "Start_Time" AS start_time,
    "End_Time" AS end_time,
    "Academic_Level" AS academic_level,
    "Subject_Code" AS subject_code,
    "Paper_No" AS paper_no,
    "Subject_Name" AS subject_name,
    "MOA" AS moa,
    "Duration" AS duration
FROM "sg-data-d-e6809acbf96c701093bc673c475755e0"
