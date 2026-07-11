-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source combines workforce measures across workbook sections with repeated labels; do not aggregate across series without first selecting compatible measures.
SELECT
    "source_file",
    "sheet",
    "series",
    "period",
    "value"
FROM "nhs-england-dental-workforce"
