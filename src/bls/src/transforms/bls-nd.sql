-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `period` mixes regular observations with BLS aggregate period codes — M13 (annual average). `period_start_date` is derived as the first day of the observation period, so an aggregate row lands on the same date as the year's first regular row (M13/S01/S03/A01 and Q05 all stamp January 1). Filter on `period` — grouping or summing by `period_start_date` alone double-counts.
-- caution: `value` is untyped across rows: what it measures is selected by `product_code` (which product line's index). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: Index values are only comparable within one `base_date`; `industry_code`/`product_code` form a hierarchy whose parent rows contain their components.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "industry_code",
    "industry_name",
    "product_code",
    "seasonal",
    "seasonal_name",
    CAST("base_date" AS BIGINT) AS base_date,
    "series_title"
FROM "bls-nd"
