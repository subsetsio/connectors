-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sector",
    "lqt",
    "emission_factor_so4_t_c_tj",
    "emission_factor_nox_t_c_tj",
    "emission_factor_nmvoc_t_c_tj",
    "emission_factor_n2ot_c_tj",
    "emission_factor_ch4_t_c_tj",
    "emission_factor_co2_t_c_tj",
    "fuel_calorific_value_mj_nm3"
FROM "qatar-planning-and-statistics-authority-weighted-country-specific-ghg-emission-factors-computed-for-qatar"
