-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix overall, category, indicator, subindicator, and question-level scores in the GHS Index hierarchy; filter `level` or specific `indicator_code` values before aggregating.
SELECT
    "country",
    "year",
    "indicator_code",
    "indicator_label",
    "level",
    "score"
FROM "ghs-index-ghs-index-scores"
