-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `data_type_code` and `case_type_code` (case counts vs incidence rates). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `industry_code`/`supersector_code` form a NAICS hierarchy whose parent rows already contain their component industries.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "seasonal",
    "seasonal_name",
    "supersector_code",
    "supersector_name",
    "industry_code",
    "data_type_code",
    "data_type_name",
    "case_type_code",
    "case_type_name",
    "area_code",
    "area_name",
    "series_title"
FROM "bls-is"
