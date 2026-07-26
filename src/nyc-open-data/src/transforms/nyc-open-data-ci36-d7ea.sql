-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "school_type",
    "enrollment",
    "survey_pp_ri",
    "survey_pp_ct",
    "survey_pp_se",
    "survey_pp_es",
    "survey_pp_sf",
    "survey_pp_tr",
    "qr_1_1",
    "qr_1_2",
    "qr_2_2",
    "qr_3_4",
    "qr_4_2",
    "qr_1_4",
    "qr_1_3",
    "qr_3_1",
    "qr_4_1",
    "qr_5_1",
    "dates_of_review",
    "rating_ela_grade_8_pct_rs",
    "rating_mth_grade_8_pct_rs",
    "gender_female_pct",
    "gender_male_pct",
    "ell",
    "iep",
    "cap_sc_pct"
FROM "nyc-open-data-ci36-d7ea"
