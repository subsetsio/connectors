-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "trademark_class",
    "trademark_filings",
    "rank"
FROM "sg-data-d-8a9e6f514ab983ef97bffa407573ae57"
