-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sheet",
    "row_idx",
    CAST("period" AS BIGINT) AS period,
    "period_date",
    "series",
    "value",
    "value_text"
FROM "sf-fed-twelfth-district-business-sentiment"
