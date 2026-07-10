-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "ACO_ID" AS aco_id,
    "Aff_LBN" AS aff_lbn,
    "ACO_Name" AS aco_name,
    "ACO_Service_Area" AS aco_service_area,
    CAST("Agreement_Period_Num" AS BIGINT) AS agreement_period_num,
    "Initial_Start_Date" AS initial_start_date,
    "Current_Start_Date" AS current_start_date,
    CAST("Re-entering_ACO" AS BIGINT) AS re_entering_aco,
    CAST("BASIC_Track" AS BIGINT) AS basic_track,
    "BASIC_Track_Level" AS basic_track_level,
    CAST("ENHANCED_Track" AS BIGINT) AS enhanced_track,
    CAST("High_Revenue_ACO" AS BIGINT) AS high_revenue_aco,
    CAST("Low_Revenue_ACO" AS BIGINT) AS low_revenue_aco,
    CAST("Adv_Pay" AS BIGINT) AS adv_pay,
    CAST("AIM" AS BIGINT) AS aim,
    CAST("AIP" AS BIGINT) AS aip,
    CAST("PSS" AS BIGINT) AS pss,
    CAST("SNF_3-Day_Rule_Waiver" AS BIGINT) AS snf_3_day_rule_waiver,
    CAST("Prospective_Assignment" AS BIGINT) AS prospective_assignment,
    CAST("Retrospective_Assignment" AS BIGINT) AS retrospective_assignment,
    "ACO_Address" AS aco_address,
    "ACO_Public_Reporting_Website" AS aco_public_reporting_website,
    "ACO_Exec_Name" AS aco_exec_name,
    "ACO_Exec_Email" AS aco_exec_email,
    "ACO_Exec_Phone" AS aco_exec_phone,
    "ACO_Public_Name" AS aco_public_name,
    "ACO_Public_Email" AS aco_public_email,
    "ACO_Public_Phone" AS aco_public_phone,
    "ACO_Compliance_Contact_Name" AS aco_compliance_contact_name,
    "ACO_Medical_Director_Name" AS aco_medical_director_name,
    CAST("pc_flex_agreement_status" AS BIGINT) AS pc_flex_agreement_status
FROM "cms-5b227bd9-82d4-4145-86fd-809e02ca7f18"
