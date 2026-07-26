-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "category",
    "subcategory",
    "work_type",
    "fy25",
    "fy26",
    "fy27",
    "fy28",
    "fy29",
    "total"
FROM "nyc-open-data-24nr-gahi"
