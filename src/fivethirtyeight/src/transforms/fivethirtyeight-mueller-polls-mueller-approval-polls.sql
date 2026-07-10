-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Start" AS start,
    "End" AS end,
    "Pollster" AS pollster,
    "Sample Size" AS sample_size,
    "Population" AS population,
    "Text" AS text,
    "Approve" AS approve,
    "Disapprove" AS disapprove,
    "Unsure" AS unsure,
    "Approve (Republican)" AS approve_republican,
    "Approve (Democrat)" AS approve_democrat,
    "Url" AS url
FROM "fivethirtyeight-mueller-polls-mueller-approval-polls"
