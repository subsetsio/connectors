-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the source codebook for Transparency Exercise items and dimensions; it is a lookup table rather than a measured statistical series.
SELECT
    "csv_file",
    "template",
    CAST("item" AS BIGINT) AS item,
    "category",
    "label"
FROM "eba-te-data-dictionary"
