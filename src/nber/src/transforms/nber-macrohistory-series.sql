-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the series catalog; join or filter with the observations table before interpreting measured values.
SELECT
    "series_id",
    "chapter",
    "chapter_name",
    "frequency",
    "title",
    "units",
    "area",
    "source"
FROM "nber-macrohistory-series"
