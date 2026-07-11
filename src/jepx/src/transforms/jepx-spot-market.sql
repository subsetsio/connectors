-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is one half-hour delivery slot; daily or longer summaries should aggregate across all slots for each delivery_date rather than treating prices as daily observations.
SELECT
    strptime("delivery_date", '%Y/%m/%d')::DATE AS delivery_date,
    "slot",
    "sell_bid_volume_kwh",
    "buy_bid_volume_kwh",
    "contract_volume_kwh",
    "system_price",
    "area_price_hokkaido",
    "area_price_tohoku",
    "area_price_tokyo",
    "area_price_chubu",
    "area_price_hokuriku",
    "area_price_kansai",
    "area_price_chugoku",
    "area_price_shikoku",
    "area_price_kyushu"
FROM "jepx-spot-market"
