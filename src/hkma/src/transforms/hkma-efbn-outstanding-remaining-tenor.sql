-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "efb_1y_or_below",
    "efn_1y_or_below",
    "efn_1yto3y",
    "efn_3yto5y",
    "efn_5yto7y",
    "efn_7yto10y",
    "efn_10y",
    "efn_subtotal",
    "efbn_total"
FROM "hkma-efbn-outstanding-remaining-tenor"
