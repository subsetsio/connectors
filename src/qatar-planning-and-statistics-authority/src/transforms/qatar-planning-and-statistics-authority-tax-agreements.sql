-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "number_of_double_taxation_avoidance_agreements_protocols_signed",
    "dd_ltfqyt_wlbrwtwkwlt_tjnb_lzdwj_ldryby_lmwq",
    "automatic_exchange_of_information_transactions_common_reporting_standard_crs_aeoi"
FROM "qatar-planning-and-statistics-authority-tax-agreements"
