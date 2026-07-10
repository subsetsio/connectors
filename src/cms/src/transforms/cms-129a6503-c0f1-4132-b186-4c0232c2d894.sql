-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Provider Number" AS provider_number,
    "Facility Name" AS facility_name,
    "City" AS city,
    "State" AS state,
    "Zip Code" AS zip_code,
    "Certification Date" AS certification_date,
    CAST("Medicare Census" AS BIGINT) AS medicare_census,
    CAST("Medicaid Census" AS BIGINT) AS medicaid_census,
    CAST("Other Census" AS BIGINT) AS other_census,
    CAST("Total Residents" AS BIGINT) AS total_residents,
    "Program Participation Code" AS program_participation_code,
    "Hospital Based" AS hospital_based,
    "Ownership Type" AS ownership_type,
    "Multi-Facility Organization" AS multi_facility_organization,
    "Multi-Facility Organization Name" AS multi_facility_organization_name,
    CAST("Number of AIDS Beds" AS BIGINT) AS number_of_aids_beds,
    CAST("Number of Alzheimer's Disease Beds" AS BIGINT) AS number_of_alzheimer_s_disease_beds,
    CAST("Number of Dialysis Beds" AS BIGINT) AS number_of_dialysis_beds,
    CAST("Number of Disabled Children/Young Adult Beds" AS BIGINT) AS number_of_disabled_children_young_adult_beds,
    CAST("Number of Head Trauma Beds" AS BIGINT) AS number_of_head_trauma_beds,
    CAST("Number of Hospice Beds" AS BIGINT) AS number_of_hospice_beds,
    CAST("Number of Huntington's Disease Beds" AS BIGINT) AS number_of_huntington_s_disease_beds,
    CAST("Number of Ventilator Beds" AS BIGINT) AS number_of_ventilator_beds,
    CAST("Number of Other Specialized Rehab Beds" AS BIGINT) AS number_of_other_specialized_rehab_beds,
    "Organized Residents' Group" AS organized_residents_group,
    "Organized Family Member Group" AS organized_family_member_group,
    "Facility Conducts Experimental Research" AS facility_conducts_experimental_research,
    "Continuing Care Retirement Community (CCRC)" AS continuing_care_retirement_community_ccrc,
    "7 Day RN Waiver Date" AS 7_day_rn_waiver_date,
    CAST("7 Day RN Hrs Waived Per Week" AS BIGINT) AS 7_day_rn_hrs_waived_per_week,
    "24 Hr Licensed Nursing Waiver Date" AS 24_hr_licensed_nursing_waiver_date,
    CAST("24 Hr Licensed Nursing Hrs Waived Per Week" AS BIGINT) AS 24_hr_licensed_nursing_hrs_waived_per_week,
    "Nurse Aide Training and Competency Evaluation Program" AS nurse_aide_training_and_competency_evaluation_program
FROM "cms-129a6503-c0f1-4132-b186-4c0232c2d894"
