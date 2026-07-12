-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "regional_grouping",
    "lmjmw_t_lqlymy",
    "real_gdp_growth_rate_2021",
    "real_gdp_growth_rate_2022",
    "real_gdp_growth_rate_2023",
    "cpi_y_o_y_change_2021",
    "cpi_y_o_y_change_2022",
    "cpi_y_o_y_change_2023",
    "current_account_balance_as_of_gdp_2021",
    "current_account_balance_as_of_gdp_2022",
    "current_account_balance_as_of_gdp_2023"
FROM "qatar-planning-and-statistics-authority-qatar-economic-performance-compared-with-other-regions-2021-2023"
