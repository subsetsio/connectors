-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `measure_code` and `duration_code` (index vs percent change). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: Index values are only comparable within one `base_year`.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "sector_code",
    "sector_name",
    "measure_code",
    "measure_name",
    CAST("duration_code" AS BIGINT) AS duration_code,
    "duration_name",
    "base_year",
    "series_title"
FROM "bls-mp"
