-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "RentIncrease_1" AS rentincrease_1,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-70675eng"
