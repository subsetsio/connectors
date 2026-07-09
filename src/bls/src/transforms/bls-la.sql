-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `period` mixes regular observations with BLS aggregate period codes — M13 (annual average). `period_start_date` is derived as the first day of the observation period, so an aggregate row lands on the same date as the year's first regular row (M13/S01/S03/A01 and Q05 all stamp January 1). Filter on `period` — grouping or summing by `period_start_date` alone double-counts.
-- caution: Carries both seasonally adjusted (`seasonal` = 'S') and unadjusted ('U') versions of the same underlying series; filter `seasonal` or you will mix two measurements of the same quantity.
-- caution: `value` is untyped across rows: what it measures is selected by `measure_code` (labor force, employment, unemployment, unemployment rate). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: Rows span several geographic levels at once (states, counties, cities, metro areas, census regions) — `area_code` is only unique within its `area_type_code`, so always filter or group by `area_type_code` before aggregating; county and city rows are nested inside their state's rows.
-- caution: `area_code` ships undecoded (no `area_name`): the LAUS area map is keyed on (`area_type_code`, `area_code`), so it could not be joined on `area_code` alone.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "area_type_code",
    "area_type_name",
    "area_code",
    "measure_code",
    "measure_name",
    "seasonal",
    "seasonal_name",
    "srd_code",
    "series_title"
FROM "bls-la"
