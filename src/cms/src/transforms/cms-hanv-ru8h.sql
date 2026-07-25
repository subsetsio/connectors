-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATE" AS state,
    "Lower box percent of patients-nephrologists' communication and caring" AS lower_box_pct_pts_nephrologists_communication_caring,
    "Middle box percent of patients-nephrologists' communication and caring" AS middle_box_pct_pts_nephrologists_communication_caring,
    "Top box percent of patients-nephrologists' communication and caring" AS top_box_pct_pts_nephrologists_communication_caring,
    "Linearized score of nephrologists' communication and caring" AS linearized_score_of_nephrologists_communication_and_caring,
    "Lower box percent of patients-quality of dialysis center care and operations" AS lower_box_pct_pts_quality_dial_center_care_operations,
    "Middle box percent of patients-quality of dialysis center care and operations" AS middle_box_pct_pts_quality_dial_center_care_operations,
    "Top box percent of patients-quality of dialysis center care and operations" AS top_box_pct_pts_quality_dial_center_care_operations,
    "Linearized score of quality of dialysis center care and operations" AS linearized_score_quality_dial_center_care_operations,
    "Lower box percent of patients-providing information to patients" AS lower_box_percent_of_patients_providing_information_to_patients,
    "Top box percent of patients- providing information to patients" AS top_box_percent_of_patients_providing_information_to_patients,
    "Linearized score of providing information to patients" AS linearized_score_of_providing_information_to_patients,
    "Lower box percent of patients-rating of the nephrologist" AS lower_box_percent_of_patients_rating_of_the_nephrologist,
    "Middle box percent of patients- rating of the nephrologist" AS middle_box_percent_of_patients_rating_of_the_nephrologist,
    "Top box percent of patients- rating of the nephrologist" AS top_box_percent_of_patients_rating_of_the_nephrologist,
    "Linearized score of rating of the nephrologist" AS linearized_score_of_rating_of_the_nephrologist,
    "Lower box percent of patients-rating of the dialysis center staff" AS lower_box_pct_pts_rating_dial_center_staff,
    "Middle box percent of patients-rating of the dialysis center staff" AS middle_box_pct_pts_rating_dial_center_staff,
    "Top box percent of patients-rating of the dialysis center staff" AS top_box_percent_of_patients_rating_of_the_dialysis_center_staff,
    "Linearized score of rating of the dialysis center staff" AS linearized_score_of_rating_of_the_dialysis_center_staff,
    "Lower box percent of patients-rating of the dialysis facility" AS lower_box_percent_of_patients_rating_of_the_dialysis_facility,
    "Middle box percent of patients-rating of the dialysis facility" AS middle_box_percent_of_patients_rating_of_the_dialysis_facility,
    "Top box percent of patients-rating of the dialysis facility" AS top_box_percent_of_patients_rating_of_the_dialysis_facility,
    "Linearized score of rating of the dialysis facility" AS linearized_score_of_rating_of_the_dialysis_facility,
    "Total number of completed interviews from the Fall and Spring Surveys" AS total_num_completed_interviews_from_fall_spring_surveys,
    "Survey response rate" AS survey_response_rate
FROM "cms-hanv-ru8h"
