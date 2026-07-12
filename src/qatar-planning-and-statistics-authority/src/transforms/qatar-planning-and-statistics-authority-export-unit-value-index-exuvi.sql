-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code",
    "group_desc_en",
    "group_desc_ar",
    "weight",
    "q1_2020",
    "q2_2020",
    "q3_2020",
    "q4_2020",
    "q1_2021",
    "q2_2021",
    "q3_2021",
    "q4_2021",
    "q1_2022",
    "q2_2022",
    "q3_2022",
    "q4_2022",
    "q1_2023",
    "q2_2023",
    "q3_2023",
    "q4_2023",
    "q1_2024",
    "q2_2024",
    "q3_2024",
    "q4_2024"
FROM "qatar-planning-and-statistics-authority-export-unit-value-index-exuvi"
