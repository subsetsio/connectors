-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_day",
    "efb_7d",
    "efb_30d",
    "efb_91d",
    "efb_182d",
    "efb_273d",
    "efb_364d",
    "efn_2y",
    "efn_3y",
    "efn_4y",
    "efn_5y",
    "efn_7y",
    "efn_10y",
    "efn_15y"
FROM "hkma-efbn-yield-daily"
