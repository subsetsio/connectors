-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "COUNTRY" AS country,
    CAST("Lower box percent of patients-nephrologists' communication and caring" AS DOUBLE) AS lower_box_percent_of_patients_nephrologists_communication_and_caring,
    CAST("Middle box percent of patients-nephrologists' communication and caring" AS DOUBLE) AS middle_box_percent_of_patients_nephrologists_communication_and_caring,
    CAST("Top box percent of patients-nephrologists' communication and caring" AS DOUBLE) AS top_box_percent_of_patients_nephrologists_communication_and_caring,
    CAST("Linearized score of nephrologists' communication and caring" AS DOUBLE) AS linearized_score_of_nephrologists_communication_and_caring,
    CAST("Lower box percent of patients-quality of dialysis center care and operations" AS DOUBLE) AS lower_box_percent_of_patients_quality_of_dialysis_center_care_and_operations,
    CAST("Middle box percent of patients-quality of dialysis center care and operations" AS DOUBLE) AS middle_box_percent_of_patients_quality_of_dialysis_center_care_and_operations,
    CAST("Top box percent of patients-quality of dialysis center care and operations" AS DOUBLE) AS top_box_percent_of_patients_quality_of_dialysis_center_care_and_operations,
    CAST("Linearized score of quality of dialysis center care and operations" AS DOUBLE) AS linearized_score_of_quality_of_dialysis_center_care_and_operations,
    CAST("Lower box percent of patients-providing information to patients" AS DOUBLE) AS lower_box_percent_of_patients_providing_information_to_patients,
    CAST("Top box percent of patients- providing information to patients" AS DOUBLE) AS top_box_percent_of_patients_providing_information_to_patients,
    CAST("Linearized score of providing information to patients" AS DOUBLE) AS linearized_score_of_providing_information_to_patients,
    CAST("Lower box percent of patients-rating of the nephrologist" AS DOUBLE) AS lower_box_percent_of_patients_rating_of_the_nephrologist,
    CAST("Middle box percent of patients- rating of the nephrologist" AS DOUBLE) AS middle_box_percent_of_patients_rating_of_the_nephrologist,
    CAST("Top box percent of patients- rating of the nephrologist" AS DOUBLE) AS top_box_percent_of_patients_rating_of_the_nephrologist,
    CAST("Linearized score of rating of the nephrologist" AS DOUBLE) AS linearized_score_of_rating_of_the_nephrologist,
    CAST("Lower box percent of patients-rating of the dialysis center staff" AS DOUBLE) AS lower_box_percent_of_patients_rating_of_the_dialysis_center_staff,
    CAST("Middle box percent of patients-rating of the dialysis center staff" AS DOUBLE) AS middle_box_percent_of_patients_rating_of_the_dialysis_center_staff,
    CAST("Top box percent of patients-rating of the dialysis center staff" AS DOUBLE) AS top_box_percent_of_patients_rating_of_the_dialysis_center_staff,
    CAST("Linearized score of rating of the dialysis center staff" AS DOUBLE) AS linearized_score_of_rating_of_the_dialysis_center_staff,
    CAST("Lower box percent of patients-rating of the dialysis facility" AS DOUBLE) AS lower_box_percent_of_patients_rating_of_the_dialysis_facility,
    CAST("Middle box percent of patients-rating of the dialysis facility" AS DOUBLE) AS middle_box_percent_of_patients_rating_of_the_dialysis_facility,
    CAST("Top box percent of patients-rating of the dialysis facility" AS DOUBLE) AS top_box_percent_of_patients_rating_of_the_dialysis_facility,
    CAST("Linearized score of rating of the dialysis facility" AS DOUBLE) AS linearized_score_of_rating_of_the_dialysis_facility,
    CAST("Total number of completed interviews from the Fall and Spring Surveys" AS DOUBLE) AS total_number_of_completed_interviews_from_the_fall_and_spring_surveys,
    CAST("Survey response rate" AS DOUBLE) AS survey_response_rate
FROM "cms-utgq-v46w"
