-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "gross_domestic_expenditure_on_r_d_in_million_euro",
    "gross_domestic_expenditure_on_r_d_funded_by_federal_government_in_million_euro",
    "gross_domestic_expenditure_on_r_d_funded_by_research_premium_in_million_euro",
    "gross_domestic_expenditure_on_r_d_funded_by_l_nder_governments_in_million_euro",
    "gross_domestic_expenditure_on_r_d_funded_by_business_enterprise_sector_in_million_euro",
    "gross_domestic_expenditure_on_r_d_funded_by_abroad_in_million_euro",
    "gross_domestic_expenditure_on_r_d_funded_by_other_in_million_euro",
    "nominal_gross_domestic_product_gdp_in_billion_euro",
    "gerd_as_a_percentage_of_gdp_research_intensity"
FROM "statistics-austria-ogd-f1902fuequote-fuequote-1"
