-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("﻿time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    CAST("elgs_expected_number" AS BIGINT) AS elgs_expected_number,
    "elg_listening_attention_understanding",
    "elg_speaking",
    "elg_self_regulation",
    "elg_managing_self",
    "elg_building_relationships",
    "elg_gross_motor_skills",
    "elg_fine_motor_skills",
    "elg_comprehension",
    "elg_word_reading",
    "elg_writing",
    "elg_number",
    "elg_numerical_patterns",
    CAST("elg_combination_children_count" AS BIGINT) AS elg_combination_children_count,
    CAST("elg_number_children_count" AS BIGINT) AS elg_number_children_count,
    CAST("elg_combination_number_children_percent" AS DOUBLE) AS elg_combination_number_children_percent
FROM "dfe-019ac0fc-5621-74a8-8351-f75f1fb1757c"
