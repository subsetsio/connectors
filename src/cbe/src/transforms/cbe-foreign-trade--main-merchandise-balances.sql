-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains related merchandise balance measures that should not be summed together without selecting an `indicator_en` measure.
-- caution: Rows combine annual and quarterly observations; use `frequency` to avoid mixing time granularities.
SELECT
    "indicator_en",
    "indicator_ar",
    "dimension",
    "period_label",
    "frequency",
    "year",
    "date",
    "value",
    "source_file"
FROM "cbe-foreign-trade--main-merchandise-balances"
