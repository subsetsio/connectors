-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "version",
    "sex",
    "disadvantage_status",
    "ethnicity_minor",
    "sen_provision",
    "exam_cohort",
    "aps_per_entry_student_count",
    "aps_per_entry",
    "aps_per_entry_grade",
    "two_or_more_level3_percent",
    "one_or_more_alevel_or_applied_student_count",
    "best_three_alevels_aps",
    "best_three_alevels_grade",
    "three_astar_to_a_percent",
    "aab_percent",
    "one_or_more_alevel_student_count",
    "aab_two_facilitating_percent",
    "level3_voc_not_applied_general_student_count",
    "level3_voc_tech_level_percent",
    "level3_voc_not_tech_level_student_count",
    "level3_voc_applied_general_percent",
    "level2_highest_entry_student_count",
    "level2_techcert_percent"
FROM "dfe-019d9130-da65-77f6-a2b6-ee939ad5449f"
