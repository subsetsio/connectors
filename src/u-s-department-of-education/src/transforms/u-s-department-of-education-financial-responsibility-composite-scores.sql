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
    "Composite Scores For Private, Non-Profit and Proprietary Institutions with Fiscal Years Ending Between 7/1/2017 and 6/30/2018 Grouped by: State, Institution Name Data Source: eZ-Audit as of September 18, 2020" AS composite_scores_for_private_non_profit_and_proprietary_institutions_with_fiscal_years_ending_between_7_1_2017_and_6_30_2018_grouped_by_state_institution_name_data_source_ez_audit_as_of_september_18_2020,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Unnamed: 9" AS unnamed_9,
    "Composite Scores For Private, Non-Profit and Proprietary Institutions with Fiscal Years Ending Between 7/1/2016 and 6/30/2017 Grouped by: State, Institution Name Data Source: eZ-Audit August 14, 2019" AS composite_scores_for_private_non_profit_and_proprietary_institutions_with_fiscal_years_ending_between_7_1_2016_and_6_30_2017_grouped_by_state_institution_name_data_source_ez_audit_august_14_2019,
    "Composite Scores For Private, Non-Profit and Proprietary Institutions with Fiscal Years Ending Between 7/1/2015 and 6/30/2016 Grouped by: State, Institution Name Data Source: eZ-Audit May 1, 2018" AS composite_scores_for_private_non_profit_and_proprietary_institutions_with_fiscal_years_ending_between_7_1_2015_and_6_30_2016_grouped_by_state_institution_name_data_source_ez_audit_may_1_2018,
    "Composite Scores For Private Non-Profit and Proprietary Institutions with Fiscal Years Ending Between 7/1/2014 and 6/30/2015 Grouped by: State, Institution Name Data Source: eZ-Audit August 22, 2016" AS composite_scores_for_private_non_profit_and_proprietary_institutions_with_fiscal_years_ending_between_7_1_2014_and_6_30_2015_grouped_by_state_institution_name_data_source_ez_audit_august_22_2016,
    "Unnamed: 1" AS unnamed_1,
    "Composite Scores For Private Non-Profit and Proprietary Institutions with Fiscal Years Ending Between 7/1/2013 and 6/30/2014 Grouped by: State, Institution Name Data Source: eZ-Audit 9/08/2015" AS composite_scores_for_private_non_profit_and_proprietary_institutions_with_fiscal_years_ending_between_7_1_2013_and_6_30_2014_grouped_by_state_institution_name_data_source_ez_audit_9_08_2015,
    "Composite Scores For Private Non-Profit and Proprietary Institutions with Fiscal Years Ending Between 7/1/2012 and 6/30/2013 Grouped by: State, Institution Name Data Source: eZ-Audit 8/26/2014" AS composite_scores_for_private_non_profit_and_proprietary_institutions_with_fiscal_years_ending_between_7_1_2012_and_6_30_2013_grouped_by_state_institution_name_data_source_ez_audit_8_26_2014
FROM "u-s-department-of-education-financial-responsibility-composite-scores"
