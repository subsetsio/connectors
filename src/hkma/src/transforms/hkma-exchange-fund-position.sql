-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "unaudited_figures",
    "assets_fc",
    "assets_hkd",
    "assets_total",
    "liab_cert_of_indebt",
    "liab_gov_iss_curr_notes",
    "liab_banking_system_bal",
    "liab_ef_bills_notes_iss",
    "liab_fiscal_resv",
    "liab_other_instit",
    "liab_pla_bank_oth_fin_instit",
    "liab_govfunds_statubodies",
    "liab_subsidiaries",
    "liab_other",
    "liab_total",
    "fund_equity"
FROM "hkma-exchange-fund-position"
