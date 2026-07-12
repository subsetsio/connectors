-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table inventories official TED CSV subset download packages; it does not contain the notice-level rows inside each ZIP package.
SELECT
    "asset_id",
    "dataset_id",
    "title",
    "format",
    "url",
    "filename",
    "notice_kind",
    "period_start_year",
    "period_end_year",
    "is_deprecated",
    "issued",
    "modified"
FROM "ted-eu-procurement-csv-subset"
