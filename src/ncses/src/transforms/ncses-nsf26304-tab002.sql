-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Survey population and fiscal year - All institutions" AS survey_population_and_fiscal_year_all_institutions,
    "All R and D expenditures - All institutions" AS all_r_and_d_expenditures_all_institutions,
    "Source of funds - Federal government - All institutions" AS source_of_funds_federal_government_all_institutions,
    "Source of funds - State and local government - All institutions" AS source_of_funds_state_and_local_government_all_institutions,
    "Source of funds - Institution funds - Total - All institutions" AS source_of_funds_institution_funds_total_all_institutions,
    "Source of funds - Institution funds - Institutionally financed research - All institutions" AS source_of_funds_institution_funds_institutionally_financed_research_all_institutions,
    "Source of funds - Institution funds - Cost sharing - All institutions" AS source_of_funds_institution_funds_cost_sharing_all_institutions,
    "Source of funds - Institution funds - Unrecovered indirect costs - All institutions" AS source_of_funds_institution_funds_unrecovered_indirect_costs_all_institutions,
    "Source of funds - Business - Unrecovered indirect costs - All institutions" AS source_of_funds_business_unrecovered_indirect_costs_all_institutions,
    "Source of funds - Nonprofit organizations - Unrecovered indirect costs - All institutions" AS source_of_funds_nonprofit_organizations_unrecovered_indirect_costs_all_institutions,
    "Source of funds - All other sources - Unrecovered indirect costs - All institutions" AS source_of_funds_all_other_sources_unrecovered_indirect_costs_all_institutions
FROM "ncses-nsf26304-tab002"
