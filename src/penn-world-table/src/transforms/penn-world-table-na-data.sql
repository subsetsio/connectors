-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: National-accounts variables mix current-price, constant-price and growth-rate concepts; choose compatible columns before comparing levels or rates.
SELECT
    "countrycode",
    "year",
    "v_c",
    "v_i",
    "v_g",
    "v_x",
    "v_m",
    "v_gdp",
    "q_c",
    "q_i",
    "q_g",
    "q_x",
    "q_m",
    "q_gdp",
    "pop",
    "xr",
    "xr2",
    "v_gfcf",
    "q_gfcf",
    "emp",
    "avh"
FROM "penn-world-table-na-data"
