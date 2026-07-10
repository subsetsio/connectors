-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "investigation",
    "investigation-start" AS investigation_start,
    "investigation-end" AS investigation_end,
    "investigation-days" AS investigation_days,
    "name",
    "indictment-days " AS indictment_days,
    "type",
    "cp-date" AS cp_date,
    "cp-days" AS cp_days,
    "overturned",
    "pardoned",
    "american",
    "president"
FROM "fivethirtyeight-russia-investigation-russia-investigation"
