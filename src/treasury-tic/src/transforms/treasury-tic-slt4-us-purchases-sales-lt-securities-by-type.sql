-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country column includes jurisdictions and aggregate categories alongside countries, so filter to the desired geography level before summing across countries.
SELECT
    "country",
    CAST("country_code" AS BIGINT) AS country_code,
    strptime("date", '%Y-%m')::DATE AS date,
    "for_lt_total_sale",
    "for_lt_treas_sale",
    "for_lt_agcy_sale",
    "for_lt_corp_sale",
    "for_lt_eqty_sale",
    "us_lt_total_sale",
    "us_lt_govt_bond_sale",
    "us_lt_corp_bond_sale",
    "us_lt_eqty_sale",
    "for_lt_total_pur",
    "for_lt_treas_pur",
    "for_lt_agcy_pur",
    "for_lt_corp_pur",
    "for_lt_eqty_pur",
    "us_lt_total_pur",
    "us_lt_govt_bond_pur",
    "us_lt_corp_bond_pur",
    "us_lt_eqty_pur"
FROM "treasury-tic-slt4-us-purchases-sales-lt-securities-by-type"
