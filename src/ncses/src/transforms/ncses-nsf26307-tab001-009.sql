-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "All science engineering and health graduate students - Total" AS all_science_engineering_and_health_graduate_students_total,
    "All science engineering and health graduate students - Full time - Number" AS all_science_engineering_and_health_graduate_students_full_time_number,
    "All science engineering and health graduate students - Full time - Percent" AS all_science_engineering_and_health_graduate_students_full_time_percent,
    "All science engineering and health graduate students - Part time - Number" AS all_science_engineering_and_health_graduate_students_part_time_number,
    "All science engineering and health graduate students - Part time - Percent" AS all_science_engineering_and_health_graduate_students_part_time_percent,
    "All science graduate students - Total - Percent" AS all_science_graduate_students_total_percent,
    "All science graduate students - Full time - Number" AS all_science_graduate_students_full_time_number,
    "All science graduate students - Full time - Percent" AS all_science_graduate_students_full_time_percent,
    "All science graduate students - Part time - Number" AS all_science_graduate_students_part_time_number,
    "All science graduate students - Part time - Percent" AS all_science_graduate_students_part_time_percent,
    "All engineering graduate students - Total - Percent" AS all_engineering_graduate_students_total_percent,
    "All engineering graduate students - Full time - Number" AS all_engineering_graduate_students_full_time_number,
    "All engineering graduate students - Full time - Percent" AS all_engineering_graduate_students_full_time_percent,
    "All engineering graduate students - Part time - Number" AS all_engineering_graduate_students_part_time_number,
    "All engineering graduate students - Part time - Percent" AS all_engineering_graduate_students_part_time_percent,
    "All health graduate students - Total - Percent" AS all_health_graduate_students_total_percent,
    "All health graduate students - Full time - Number" AS all_health_graduate_students_full_time_number,
    "All health graduate students - Full time - Percent" AS all_health_graduate_students_full_time_percent,
    "All health graduate students - Part time - Number" AS all_health_graduate_students_part_time_number,
    "All health graduate students - Part time - Percent" AS all_health_graduate_students_part_time_percent
FROM "ncses-nsf26307-tab001-009"
