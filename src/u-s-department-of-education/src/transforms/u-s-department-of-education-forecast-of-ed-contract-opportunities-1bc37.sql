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
    "Forecast of Prime Contracting Opportunities for FY 2017" AS forecast_of_prime_contracting_opportunities_for_fy_2017,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Unnamed: 9" AS unnamed_9,
    "Unnamed: 10" AS unnamed_10,
    "Unnamed: 11" AS unnamed_11,
    "Unnamed: 12" AS unnamed_12,
    "Unnamed: 13" AS unnamed_13,
    "Unnamed: 14" AS unnamed_14,
    "Unnamed: 15" AS unnamed_15,
    "Unnamed: 16" AS unnamed_16,
    "Unnamed: 17" AS unnamed_17,
    "Unnamed: 18" AS unnamed_18,
    "Unnamed: 19" AS unnamed_19,
    "Forecast of Prime Contracting Opportunities for FY 2020" AS forecast_of_prime_contracting_opportunities_for_fy_2020,
    "Forecast of Prime Contracting Opportunities for FY 2021" AS forecast_of_prime_contracting_opportunities_for_fy_2021,
    "Contract Type (Award or IDV Type Description)" AS contract_type_award_or_idv_type_description,
    "Type of Competition" AS type_of_competition,
    "Anticipated Contract Action Type Code" AS anticipated_contract_action_type_code,
    "Estimated Value of Contract $ Range" AS estimated_value_of_contract_range,
    "Estimated Current Fiscal Year $ Range" AS estimated_current_fiscal_year_range,
    "Estimated Solicitation Date" AS estimated_solicitation_date,
    "Target Award Date" AS target_award_date
FROM "u-s-department-of-education-forecast-of-ed-contract-opportunities-1bc37"
