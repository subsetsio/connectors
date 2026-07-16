-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "BenzineEuro95_1" AS benzineeuro95_1,
    "Diesel_2" AS diesel_2,
    "Lpg_3" AS lpg_3,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80416ned"
