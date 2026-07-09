-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `datatype_code` (employment, mean wage, wage percentiles). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `area_code` ships undecoded (no `area_name`): the OES area map is keyed on (`state_code`, `areatype_code`, `area_code`), so it could not be joined on `area_code` alone; use `areatype_code` + `state_code` to interpret it.
-- caution: `occupation_code` is a SOC hierarchy (major groups contain detailed occupations) and `industry_code` carries cross-industry totals — summing employment across either double-counts.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    CAST("footnote_codes" AS BIGINT) AS footnote_codes,
    "seasonal",
    "seasonal_name",
    "areatype_code",
    "areatype_name",
    "industry_code",
    "industry_name",
    "occupation_code",
    "occupation_name",
    "datatype_code",
    "datatype_name",
    "state_code",
    "area_code",
    "sector_code",
    "sector_name",
    "series_title"
FROM "bls-oe"
