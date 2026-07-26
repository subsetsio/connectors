-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "program_category",
    "code",
    "fy25",
    "fy26",
    "fy27",
    "fy28",
    "fy29",
    "total"
FROM "nyc-open-data-9ddq-vbjj"
