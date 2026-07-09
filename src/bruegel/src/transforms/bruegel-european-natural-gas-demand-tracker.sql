-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Value is a deviation in TWh against the 2019-2021 monthly-average baseline, not a demand level. Both dimensions carry aggregates alongside their components: country includes an EU row, and sector includes total and combined categories next to component sectors. Filter both before summing.
SELECT
    "date",
    "country",
    "sector",
    "value"
FROM "bruegel-european-natural-gas-demand-tracker"
