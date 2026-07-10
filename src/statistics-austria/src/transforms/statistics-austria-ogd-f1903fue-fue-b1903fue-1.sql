-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "industries_nace_2008",
    "number_of_r_d_performing_enterprises",
    "headcounts_for_r_d_total",
    "headcounts_for_r_d_researchers",
    "headcounts_for_r_d_technicians",
    "headcounts_for_r_d_other_supporting_staff",
    "fte_for_r_d_total",
    "fte_for_r_d_male_total",
    "fte_for_r_d_female_total",
    "fte_for_r_d_researchers",
    "fte_for_rad_male_researchers",
    "fte_for_r_d_female_researchers",
    "fte_for_r_d_technicians",
    "fte_for_r_d_male_technicians",
    "fte_for_r_d_female_technicians",
    "fte_for_r_d_other_supporting_staff",
    "fte_for_r_d_male_other_supporting_staff",
    "fte_for_r_d_female_other_supporting_staff",
    "fte_for_r_d_researchers_phd",
    "fte_for_r_d_researchers_master_study",
    "fte_for_r_d_researchers_bachelor_or_short_study",
    "fte_for_r_d_researchers_post_secondary_colleges",
    "fte_for_r_d_researchers_master_craftman_s_diploma",
    "fte_for_r_d_researchers_school_leaving_examination_in_a_higher_technical_or_vocational_college_e_g_bhs_htl_hak",
    "fte_for_r_d_researchers_school_leaving_examination_in_an_academic_secondary_school_e_g_ahs_bms_apprenticeship",
    "fte_for_r_d_researchers_other_education"
FROM "statistics-austria-ogd-f1903fue-fue-b1903fue-1"
