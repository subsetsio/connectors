-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "All doctoral students - Rank" AS all_doctoral_students_rank,
    "All doctoral students - Total" AS all_doctoral_students_total,
    "All doctoral students - Science" AS all_doctoral_students_science,
    "All doctoral students - Engineering" AS all_doctoral_students_engineering,
    "All doctoral students - Health" AS all_doctoral_students_health,
    "Full-time doctoral students - Rank" AS full_time_doctoral_students_rank,
    "Full-time doctoral students - Total" AS full_time_doctoral_students_total,
    "Full-time doctoral students - Science" AS full_time_doctoral_students_science,
    "Full-time doctoral students - Engineering" AS full_time_doctoral_students_engineering,
    "Full-time doctoral students - Health" AS full_time_doctoral_students_health,
    "Part-time doctoral students - Rank" AS part_time_doctoral_students_rank,
    "Part-time doctoral students - Total" AS part_time_doctoral_students_total,
    "Part-time doctoral students - Science" AS part_time_doctoral_students_science,
    "Part-time doctoral students - Engineering" AS part_time_doctoral_students_engineering,
    "Part-time doctoral students - Health" AS part_time_doctoral_students_health
FROM "ncses-nsf26307-tab004-003"
