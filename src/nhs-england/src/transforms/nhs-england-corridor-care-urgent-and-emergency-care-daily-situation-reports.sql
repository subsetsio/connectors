-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source is a daily situation-report extract with repeated labels across workbook sections; treat rows as source observations and avoid assuming a unique period/series grain.
SELECT
    "source_file",
    "sheet",
    "series",
    "period",
    "value"
FROM "nhs-england-corridor-care-urgent-and-emergency-care-daily-situation-reports"
