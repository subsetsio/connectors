-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "All graduate students - Rank" AS all_graduate_students_rank,
    "All graduate students - Total" AS all_graduate_students_total,
    "All graduate students - Science" AS all_graduate_students_science,
    "All graduate students - Engineering" AS all_graduate_students_engineering,
    "All graduate students - Health" AS all_graduate_students_health,
    "Full-time students - Rank" AS full_time_students_rank,
    "Full-time students - Total" AS full_time_students_total,
    "Full-time students - Science" AS full_time_students_science,
    "Full-time students - Engineering" AS full_time_students_engineering,
    "Full-time students - Health" AS full_time_students_health,
    "Part-time students - Rank" AS part_time_students_rank,
    "Part-time students - Total" AS part_time_students_total,
    "Part-time students - Science" AS part_time_students_science,
    "Part-time students - Engineering" AS part_time_students_engineering,
    "Part-time students - Health" AS part_time_students_health
FROM "ncses-nsf26307-tab004-001"
