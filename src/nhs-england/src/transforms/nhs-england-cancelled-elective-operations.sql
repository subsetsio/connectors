-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows represent several cancellation-related measures; filter to compatible series before comparing values.
SELECT
    "source_file",
    "sheet",
    "series",
    "period",
    "value"
FROM "nhs-england-cancelled-elective-operations"
