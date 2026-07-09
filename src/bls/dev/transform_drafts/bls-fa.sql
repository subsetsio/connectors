-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `datatype_code` and `case_code` (fatality counts vs rates). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `industry_code`, `occupation_code`, `event_code` and `area_code` each carry 'all'/'total' aggregate rows alongside their components.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "seasonal",
    "category_code",
    CAST("datatype_code" AS BIGINT) AS datatype_code,
    "datatype_name",
    "case_code",
    "case_name",
    "industry_code",
    "industry_name",
    "event_code",
    "event_name",
    "source_code",
    "source_name",
    "occupation_code",
    "occupation_name",
    "area_code",
    "area_name"
FROM "bls-fa"
