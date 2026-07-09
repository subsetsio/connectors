-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `period` mixes regular observations with BLS aggregate period codes — Q05 (annual average). `period_start_date` is derived as the first day of the observation period, so an aggregate row lands on the same date as the year's first regular row (M13/S01/S03/A01 and Q05 all stamp January 1). Filter on `period` — grouping or summing by `period_start_date` alone double-counts.
-- caution: `value` is untyped across rows: what it measures is selected by `measure_code`, `class_code` and `duration_code` (index vs percent change). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: Index values are only comparable within one `base_year`; `sector_code` carries aggregate sectors alongside their components.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    CAST("sector_code" AS BIGINT) AS sector_code,
    "sector_name",
    CAST("class_code" AS BIGINT) AS class_code,
    "class_name",
    "measure_code",
    "measure_name",
    CAST("duration_code" AS BIGINT) AS duration_code,
    "duration_name",
    "seasonal",
    "base_year"
FROM "bls-pr"
