-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "sheet_name",
    "row_number",
    "Unnamed: 0" AS unnamed_0,
    "Borrowers Identified for Forgiveness under Income Driven Repayment Adjustment by Location (Data as of early January 2025)" AS borrowers_identified_for_forgiveness_under_income_driven_repayment_adjustment_by_location_data_as_of_early_january_2025,
    "Unnamed: 2" AS unnamed_2,
    "Borrowers Identified for Forgiveness under SAVE by Location (file sent 5/22/24)" AS borrowers_identified_for_forgiveness_under_save_by_location_file_sent_5_22_24,
    "Unnamed: 4" AS unnamed_4,
    "PSLF Discharges and Approvals (PSLF, TEPSLF, and limited waiver) by Location (since 10/1/2021) Data as of early January 2025" AS pslf_discharges_and_approvals_pslf_tepslf_and_limited_waiver_by_location_since_10_1_2021_data_as_of_early_january_2025,
    "Unnamed: 6" AS unnamed_6,
    "TPD Discharges (through match with Social Security Administration and all types since 7/1/23) by Location Data as of early January 2025" AS tpd_discharges_through_match_with_social_security_administration_and_all_types_since_7_1_23_by_location_data_as_of_early_january_2025,
    "Unnamed: 8" AS unnamed_8,
    "Borrower Defense Approvals" AS borrower_defense_approvals,
    "Unnamed: 10" AS unnamed_10,
    "Borrowers Identified for Forgiveness under Income Driven Repayment Adjustment by Location (file sent 5/22/24)" AS borrowers_identified_for_forgiveness_under_income_driven_repayment_adjustment_by_location_file_sent_5_22_24,
    "PSLF Discharges and Approvals (PSLF" AS pslf_discharges_and_approvals_pslf,
    "TEPSLF" AS tepslf,
    "and limited waiver) by Location (since 10/1/2021)" AS and_limited_waiver_by_location_since_10_1_2021,
    "Borrowers with Processed PSLF Discharges (PSLF, TEPSLF, and limited waiver) by Congressional District (since 10/1/2021)" AS borrowers_with_processed_pslf_discharges_pslf_tepslf_and_limited_waiver_by_congressional_district_since_10_1_2021,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 3" AS unnamed_3,
    "and limited waiver) by Location (since 10/1/2021) Data as of early October 2024" AS and_limited_waiver_by_location_since_10_1_2021_data_as_of_early_october_2024,
    "TPD Discharges (through match with Social Security Administration and all types since 7/1/23) by Location Data as of mid-August 2024" AS tpd_discharges_through_match_with_social_security_administration_and_all_types_since_7_1_23_by_location_data_as_of_mid_august_2024,
    "Unnamed: 12" AS unnamed_12,
    "Unnamed: 13" AS unnamed_13,
    "Unnamed: 14" AS unnamed_14,
    "Unnamed: 15" AS unnamed_15,
    "Total Number of Borrowers with Approved Debt Cancellation by State" AS total_number_of_borrowers_with_approved_debt_cancellation_by_state,
    "PSLF Discharges and Approvals (PSLF, TEPSLF, and limited waiver) by Location (since 10/1/2021) Data as of early October 2024" AS pslf_discharges_and_approvals_pslf_tepslf_and_limited_waiver_by_location_since_10_1_2021_data_as_of_early_october_2024,
    "BD Approvals by State" AS bd_approvals_by_state
FROM "u-s-department-of-education-approved-debt-relief-by-state"
