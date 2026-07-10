-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_series" AS BIGINT) AS time_series,
    "general_government",
    "kategorie",
    "f_1_monetary_gold_and_special_drawing_rights_sdrs_201_in_mio_eur",
    "f_2_currency_and_deposits_202_in_mio_eur",
    "f_3_debt_securities_203_in_mio_eur",
    "f_4_loans_204_in_mio_eur",
    "f_5_equity_and_investment_fund_shares_205_in_mio_eur",
    "f_6_insurance_pensions_and_standardised_guarantee_schemes_206_in_mio_eur",
    "f_7_financial_derivatives_and_employee_stock_options_207_in_mio_eur",
    "f_8_other_accounts_payable_208_in_mio_eur",
    "sum_financial_liabilities_209_in_mln_eur"
FROM "statistics-austria-ogd-finkonseks1-fkss-quartal-1"
