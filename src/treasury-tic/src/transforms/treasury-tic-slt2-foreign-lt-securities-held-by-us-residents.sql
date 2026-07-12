-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country column includes jurisdictions and aggregate categories alongside countries, so filter to the desired geography level before summing across countries.
SELECT
    "country",
    CAST("country_code" AS BIGINT) AS country_code,
    strptime("date", '%Y-%m')::DATE AS date,
    "us_lt_total_pos",
    "us_lt_total_net",
    "us_lt_total_valchg",
    "us_lt_govt_bond_pos",
    "us_lt_govt_bond_net",
    "us_lt_govt_bond_valchg",
    "us_lt_corp_bond_pos",
    "us_lt_corp_bond_net",
    "us_lt_corp_bond_valchg",
    "us_lt_eqty_pos",
    "us_lt_eqty_net",
    "us_lt_eqty_valchg"
FROM "treasury-tic-slt2-foreign-lt-securities-held-by-us-residents"
