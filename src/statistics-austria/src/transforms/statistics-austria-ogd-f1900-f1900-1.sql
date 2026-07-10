-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "sectors_of_performance_15",
    "total_intramural_rad_expenditure_in_1000_eur",
    "basic_research_in_1000_eur",
    "basic_research_in_percent",
    "applied_research_in_1000_eur",
    "applied_research_in_percent",
    "experimental_development_in_1000_eur",
    "experimental_development_in_percent",
    "total_intramural_rae_expenditure_in_1000_eur",
    "labour_costs_in_1000_eur",
    "other_current_costs_in_1000_eur",
    "costs_for_instruments_and_equipment_in_1000_eur",
    "costs_for_buildings_and_estates_in_1000_eur",
    "source_of_funds_total_in_1000_eur",
    "business_enterprise_sector_in_1000_eur",
    "government_sector_total_in_1000_eur",
    "government_sector_federal_government_bund_in_1000_eur",
    "government_sector_regional_governments_l_nder_in_1000_eur",
    "government_sector_local_governments_gemeinden_in_1000_eur",
    "government_sector_other_in_1000_eur",
    "private_non_profit_sector_in_1000_eur",
    "abroad_incl_international_organisations_without_eu_in_1000_eur",
    "eu_in_1000_eur"
FROM "statistics-austria-ogd-f1900-f1900-1"
