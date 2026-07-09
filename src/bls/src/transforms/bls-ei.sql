-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `index_code` (which economic index). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: Index values are only comparable within one `base_period`.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "seasonal",
    "seasonal_name",
    "index_code",
    "index_name",
    "series_name",
    "base_period",
    "series_title"
FROM "bls-ei"
