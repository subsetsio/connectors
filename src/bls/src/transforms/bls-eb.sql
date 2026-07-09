-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `type_code` and `title_code` (the benefit provision measured). Never aggregate `value` without first pinning those dimensions to a single measure.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "title_code",
    "title_name",
    "type_code",
    "type_name"
FROM "bls-eb"
