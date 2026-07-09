-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `period` mixes regular observations with BLS aggregate period codes — M13 (annual average). `period_start_date` is derived as the first day of the observation period, so an aggregate row lands on the same date as the year's first regular row (M13/S01/S03/A01 and Q05 all stamp January 1). Filter on `period` — grouping or summing by `period_start_date` alone double-counts.
-- caution: Carries both seasonally adjusted (`seasonal` = 'S') and unadjusted ('U') versions of the same underlying series; filter `seasonal` or you will mix two measurements of the same quantity.
-- caution: `value` is untyped across rows: what it measures is selected by `data_type_code` (employment, hours, earnings). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `industry_code`/`supersector_code` form a NAICS hierarchy: supersector and 'Total nonfarm' rows already contain their component industries, so summing across `industry_code` double-counts.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "supersector_code",
    "supersector_name",
    "industry_code",
    "industry_name",
    "data_type_code",
    "seasonal",
    "seasonal_name",
    "series_title"
FROM "bls-ce"
