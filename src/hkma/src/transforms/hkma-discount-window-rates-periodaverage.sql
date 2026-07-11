-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The upstream period-average endpoint contains a duplicate reporting period in the raw feed, so the pass-through table is intentionally keyless.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "specific_data",
    "liquid_adj_facility_bid_rate",
    "disc_window_base_rate",
    "overnight_hibor",
    "1m_hibor_fixing",
    "liquid_adj_window_offer_rate"
FROM "hkma-discount-window-rates-periodaverage"
