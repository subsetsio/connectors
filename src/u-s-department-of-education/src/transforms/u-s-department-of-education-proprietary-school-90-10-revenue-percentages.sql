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
    "Proprietary School Revenue Percentages Report for Financial Statements with Fiscal Year Ending Dates between 07/01/17 – 06/30/18 Data Sources: eZ-Audit Date Range: 07/01/2017 through 06/30/2018 Data Extracted: 08/14/2019" AS proprietary_school_revenue_percentages_report_for_financial_statements_with_fiscal_year_ending_dates_between_07_01_17_06_30_18_data_sources_ez_audit_date_range_07_01_2017_through_06_30_2018_data_extracted_08_14_2019,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Proprietary School 90/10 Revenue Attestation Percentages" AS proprietary_school_90_10_revenue_attestation_percentages,
    "Unnamed: 0" AS unnamed_0,
    "Proprietary School Revenue Percentages Report for Financial Statements with Fiscal Year Ending Dates between 07/01/16 – 06/30/17 Data Sources: eZ-Audit Date Range: 07/01/2016 through 06/30/2017 Data Extracted: 06/14/2018" AS proprietary_school_revenue_percentages_report_for_financial_statements_with_fiscal_year_ending_dates_between_07_01_16_06_30_17_data_sources_ez_audit_date_range_07_01_2016_through_06_30_2017_data_extracted_06_14_2018,
    "Proprietary School Revenue Percentages Report for Financial Statements with Fiscal Year Ending Dates between 07/01/15 – 06/30/16 Data Sources: eZ-Audit Date Range: 07/01/2015 through 06/30/2016 Data Extracted: 06/13/2017" AS proprietary_school_revenue_percentages_report_for_financial_statements_with_fiscal_year_ending_dates_between_07_01_15_06_30_16_data_sources_ez_audit_date_range_07_01_2015_through_06_30_2016_data_extracted_06_13_2017,
    "Proprietary School Revenue Percentages Report for Financial Statements with Fiscal Year Ending Dates Between 07/01/14 –06/30/15 Data Source: EZ Audit as of June 17, 2016 Report Date: June 17, 2016 This version, posted January 6, 2017, replaces an earlier version of the report released on December 21, 2016. The current version standardizes the format for how the revenue amounts and percentages are displayed as well as making other identified adjustments that were needed in the institutional data and the summary chart." AS proprietary_school_revenue_percentages_report_for_financial_statements_with_fiscal_year_ending_dates_between_07_01_14_06_30_15_data_source_ez_audit_as_of_june_17_2016_report_date_june_17_2016_this_version_posted_january_6_2017_replaces_an_earlier_version_of_the_report_released_on_december_21_2016_the_current_version_standardizes_the_format_for_how_the_revenue_amounts_and_percentages_are_displayed_as_well_as_making_other_identified_adjustments_that_were_needed_in_the_institutional_data_and_the_summary_chart,
    "Proprietary School Revenue Percentages Report for Financial Statements with Fiscal years ending dates between 07/01/13 –06/30/14 Data Sources: NSLDS Funding File and eZ-Audit as of 6/8/15 Sorted by percentage score from highest to lowest." AS proprietary_school_revenue_percentages_report_for_financial_statements_with_fiscal_years_ending_dates_between_07_01_13_06_30_14_data_sources_nslds_funding_file_and_ez_audit_as_of_6_8_15_sorted_by_percentage_score_from_highest_to_lowest,
    "Note - Current systems do not capture actual Title IV revenues and other revenues reported by the institutions that support the calculated percentage." AS note_current_systems_do_not_capture_actual_title_iv_revenues_and_other_revenues_reported_by_the_institutions_that_support_the_calculated_percentage,
    "Proprietary School 90/10 Revenue Percentages from Financial Statements with Fiscal Year End Dates Between 7/1/2012 and 6/30/2013 Date Sources: eZ-Audit as of 7/22/2014 and Program Compliance Annual Funding Summaries" AS proprietary_school_90_10_revenue_percentages_from_financial_statements_with_fiscal_year_end_dates_between_7_1_2012_and_6_30_2013_date_sources_ez_audit_as_of_7_22_2014_and_program_compliance_annual_funding_summaries,
    "Proprietary School Revenue Percentages Report for Financial Statements with Fiscal years ending dates between 7/1/2011 – 6/30/2012 Data Sources: eZ-Audit as of 6/17/13 and Annual Funding Summaries" AS proprietary_school_revenue_percentages_report_for_financial_statements_with_fiscal_years_ending_dates_between_7_1_2011_6_30_2012_data_sources_ez_audit_as_of_6_17_13_and_annual_funding_summaries,
    "Note - current systems do not capture actual Title IV revenues and other revenues reported by the institution that support the calculated percentage." AS note_current_systems_do_not_capture_actual_title_iv_revenues_and_other_revenues_reported_by_the_institution_that_support_the_calculated_percentage,
    "Proprietary School 90/10 Revenue Percentages from Financial Statements" AS proprietary_school_90_10_revenue_percentages_from_financial_statements
FROM "u-s-department-of-education-proprietary-school-90-10-revenue-percentages"
