-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `period` mixes regular observations with BLS aggregate period codes — M13 (annual average). `period_start_date` is derived as the first day of the observation period, so an aggregate row lands on the same date as the year's first regular row (M13/S01/S03/A01 and Q05 all stamp January 1). Filter on `period` — grouping or summing by `period_start_date` alone double-counts.
-- caution: Carries both seasonally adjusted (`seasonal` = 'S') and unadjusted ('U') versions of the same underlying series; filter `seasonal` or you will mix two measurements of the same quantity.
-- caution: `value` is untyped across rows: what it measures is selected by `dataelement_code` (hires, openings, separations) and `ratelevel_code` (level vs rate). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `industry_code` and `area_code`/`state_code` both carry totals alongside their components; rate rows and level rows share the table via `ratelevel_code` and must never be summed together.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "seasonal",
    "seasonal_name",
    "industry_code",
    "industry_name",
    "state_code",
    "state_name",
    "area_code",
    "area_name",
    "sizeclass_code",
    "sizeclass_name",
    "dataelement_code",
    "dataelement_name",
    "ratelevel_code",
    "ratelevel_name"
FROM "bls-jt"
