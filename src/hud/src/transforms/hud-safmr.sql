-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Small Area Fair Market Rent rows are ZIP-code level estimates within metro-area contexts; ZIP areas are not stable administrative geographies across years.
SELECT
    "zip_code",
    "hud_area_code",
    "hud_metro_fair_market_rent_area_name",
    "safmr_0br",
    "safmr_0br_90_payment_standard",
    "safmr_0br_110_payment_standard",
    "safmr_1br",
    "safmr_1br_90_payment_standard",
    "safmr_1br_110_payment_standard",
    "safmr_2br",
    "safmr_2br_90_payment_standard",
    "safmr_2br_110_payment_standard",
    "safmr_3br",
    "safmr_3br_90_payment_standard",
    "safmr_3br_110_payment_standard",
    "safmr_4br",
    "safmr_4br_90_payment_standard",
    "safmr_4br_110_payment_standard",
    "zcta",
    "cbsasub20",
    "areaname20",
    "safmr_0br_90pct_pay_std",
    "safmr_0br_110pct_pay_std",
    "safmr_1br_90pct_pay_std",
    "safmr_1br_110pct_pay_std",
    "safmr_2br_90pct_pay_std",
    "safmr_2br_110pct_pay_std",
    "safmr_3br_90pct_pay_std",
    "safmr_3br_110pct_pay_std",
    "safmr_4br_90pct_pay_std",
    "safmr_4br_110pct_pay_std",
    "hud_fair_market_rent_area_name",
    "fiscal_year"
FROM "hud-safmr"
