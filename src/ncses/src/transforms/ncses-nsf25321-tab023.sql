-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study and primary work activity" AS field_of_study_and_primary_work_activity,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Secondary work activity - Computer applications - Number" AS secondary_work_activity_computer_applications_number,
    "Secondary work activity - Computer applications - SE" AS secondary_work_activity_computer_applications_se,
    "Secondary work activity - Design - Number" AS secondary_work_activity_design_number,
    "Secondary work activity - Design - SE" AS secondary_work_activity_design_se,
    "Secondary work activity - Management sales or administrationa - Number" AS secondary_work_activity_management_sales_or_administrationa_number,
    "Secondary work activity - Management sales or administrationa - SE" AS secondary_work_activity_management_sales_or_administrationa_se,
    "Secondary work activity - R and Db - Number" AS secondary_work_activity_r_and_db_number,
    "Secondary work activity - R and Db - SE" AS secondary_work_activity_r_and_db_se,
    "Secondary work activity - Teaching - Number" AS secondary_work_activity_teaching_number,
    "Secondary work activity - Teaching - SE" AS secondary_work_activity_teaching_se,
    "Secondary work activity - Otherc - Number" AS secondary_work_activity_otherc_number,
    "Secondary work activity - Otherc - SE" AS secondary_work_activity_otherc_se,
    "Secondary work activity - None - Number" AS secondary_work_activity_none_number,
    "Secondary work activity - None - SE" AS secondary_work_activity_none_se
FROM "ncses-nsf25321-tab023"
