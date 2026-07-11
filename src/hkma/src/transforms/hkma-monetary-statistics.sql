-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_month",
    "notes_coins_circulation",
    "aggr_balance",
    "ef_bills_notes",
    "monetary_base_total",
    "m1_total",
    "m1_hkd",
    "m2_total",
    "m2_hkd",
    "m3_total",
    "m3_hkd",
    "exrate_hkd_usd",
    "nominal_eff_exrate_index",
    "hibor_fixing_overnight",
    "hibor_fixing_3m",
    "deposit_rate_saving",
    "deposit_rate_3m",
    "yield_efpaper_3m",
    "yield_govbond_10y",
    "best_lending_rate",
    "discount_window_base_rate"
FROM "hkma-monetary-statistics"
