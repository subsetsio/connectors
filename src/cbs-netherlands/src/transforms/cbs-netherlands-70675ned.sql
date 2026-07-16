-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "Huurverhoging_1" AS huurverhoging_1,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70675ned"
