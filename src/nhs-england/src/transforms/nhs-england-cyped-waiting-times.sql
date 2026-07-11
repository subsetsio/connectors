-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The extract has repeated period/series labels across workbook context; treat rows as source observations and filter series before aggregation.
SELECT
    "source_file",
    "sheet",
    "series",
    "period",
    "value"
FROM "nhs-england-cyped-waiting-times"
