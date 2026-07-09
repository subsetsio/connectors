-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "series_code",
    "alias",
    "description",
    "units",
    "frequency",
    "period_label",
    "date",
    "value"
FROM "banco-de-espana-be1530"
