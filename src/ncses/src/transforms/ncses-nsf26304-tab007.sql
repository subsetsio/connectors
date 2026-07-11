-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Fiscal year - Total S and Ea" AS fiscal_year_total_s_and_ea,
    "Total - All R and D expenditures - Total S and Ea" AS total_all_r_and_d_expenditures_total_s_and_ea,
    "Total - Basic research - Amount - Total S and Ea" AS total_basic_research_amount_total_s_and_ea,
    "Total - Basic research - Percent - Total S and Ea" AS total_basic_research_percent_total_s_and_ea,
    "Total - Applied research and experimental development - Amount - Total S and Ea" AS total_applied_research_and_experimental_development_amount_total_s_and_ea,
    "Total - Applied research and experimental development - Percent - Total S and Ea" AS total_applied_research_and_experimental_development_percent_total_s_and_ea,
    "Federal - All federal R and D expenditures - Percent - Total S and Ea" AS federal_all_federal_r_and_d_expenditures_percent_total_s_and_ea,
    "Federal - Basic research - Amount - Total S and Ea" AS federal_basic_research_amount_total_s_and_ea,
    "Federal - Basic research - Percent - Total S and Ea" AS federal_basic_research_percent_total_s_and_ea,
    "Federal - Applied research and experimental development - Amount - Total S and Ea" AS federal_applied_research_and_experimental_development_amount_total_s_and_ea,
    "Federal - Applied research and experimental development - Percent - Total S and Ea" AS federal_applied_research_and_experimental_development_percent_total_s_and_ea
FROM "ncses-nsf26304-tab007"
