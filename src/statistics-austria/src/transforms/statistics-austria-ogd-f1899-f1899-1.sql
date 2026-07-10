-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "occupation_4",
    "headcounts_full_time_equivalents_2",
    "sectors_rad_3",
    "c_1_0_to_6_0_in_total",
    "c_1_0_to_4_0_in_total",
    "c_1_0_natural_sciences",
    "c_2_0_technical_sciences",
    "c_3_0_human_medicine_health_sciences",
    "c_4_0_agricultural_sciences_veterinary_medicine",
    "c_5_0_and_6_0_in_total",
    "c_5_0_social_sciences",
    "c_6_0_humanities"
FROM "statistics-austria-ogd-f1899-f1899-1"
