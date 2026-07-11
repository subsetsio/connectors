-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "All master's students - Rank" AS all_master_s_students_rank,
    "All master's students - Total" AS all_master_s_students_total,
    "All master's students - Science" AS all_master_s_students_science,
    "All master's students - Engineering" AS all_master_s_students_engineering,
    "All master's students - Health" AS all_master_s_students_health,
    "Full-time master's students - Rank" AS full_time_master_s_students_rank,
    "Full-time master's students - Total" AS full_time_master_s_students_total,
    "Full-time master's students - Science" AS full_time_master_s_students_science,
    "Full-time master's students - Engineering" AS full_time_master_s_students_engineering,
    "Full-time master's students - Health" AS full_time_master_s_students_health,
    "Part-time master's students - Rank" AS part_time_master_s_students_rank,
    "Part-time master's students - Total" AS part_time_master_s_students_total,
    "Part-time master's students - Science" AS part_time_master_s_students_science,
    "Part-time master's students - Engineering" AS part_time_master_s_students_engineering,
    "Part-time master's students - Health" AS part_time_master_s_students_health
FROM "ncses-nsf26307-tab004-002"
