-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Avg_No_Inmates_Engaged_in_Work_Programmes_in_YRSG_and_YRI_Works" AS avg_no_inmates_engaged_in_work_programmes_in_yrsg_and_yri_works,
    "Percentage_of_Eligible_Inmates_Engaged_in_Work_Programme" AS percentage_of_eligible_inmates_engaged_in_work_programme
FROM "sg-data-d-70c5f3868c1c2073461948dbfec4d0e8"
