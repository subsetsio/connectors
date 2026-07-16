-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "Euro95_1" AS euro95_1,
    "Diesel_2" AS diesel_2,
    "LPG_3" AS lpg_3,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80416eng"
