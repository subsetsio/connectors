-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "branches_onace_2008_50",
    "headcounts_for_r_d_total",
    "full_time_equivalents_fte_for_r_d_total",
    "r_d_full_time_equival_fte_males_in_total",
    "r_d_full_time_equival_fte_females_in_total",
    "fte_for_r_d_researchers",
    "fte_for_r_d_researchers_males",
    "fte_for_r_d_researchers_females",
    "fte_for_r_d_technicians",
    "fte_for_r_d_technicians_males",
    "fte_for_r_d_technicians_females",
    "fte_for_r_d_other_support_staff",
    "fte_for_r_d_other_support_staff_males",
    "fte_for_r_d_other_support_staff_females"
FROM "statistics-austria-ogd-f1828f2009-fue-b1828-2009-1"
