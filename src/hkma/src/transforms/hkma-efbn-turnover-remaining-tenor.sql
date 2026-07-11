-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "efb_1y_or_below_val",
    "efb_1y_or_below_vol",
    "efn_1y_or_below_val",
    "efn_1y_or_below_vol",
    "efn_1yto3y_val",
    "efn_1yto3y_vol",
    "efn_3yto5y_val",
    "efn_3yto5y_vol",
    "efn_5yto7y_val",
    "efn_5yto7y_vol",
    "efn_7yto10y_val",
    "efn_7yto10y_vol",
    "efn_10y_val",
    "efn_10y_vol",
    "efn_subtotal_val",
    "efn_subtotal_vol",
    "efbn_total_val",
    "efbn_total_vol"
FROM "hkma-efbn-turnover-remaining-tenor"
