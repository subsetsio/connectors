-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Carries both seasonally adjusted (`seasonal` = 'S') and unadjusted ('U') versions of the same underlying series; filter `seasonal` or you will mix two measurements of the same quantity.
-- caution: `value` is untyped across rows: what it measures is selected by `dataelement_code`, `dataclass_code` and `ratelevel_code` (counts vs rates). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `industry_code`, `state_code`, `msa_code` and `county_code` all carry aggregate rows alongside their components; `ratelevel_code` separates counts from rates.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    CAST("footnote_codes" AS BIGINT) AS footnote_codes,
    "seasonal",
    "seasonal_name",
    "msa_code",
    "msa_name",
    "state_code",
    "state_name",
    "county_code",
    "county_name",
    "industry_code",
    "industry_name",
    CAST("unitanalysis_code" AS BIGINT) AS unitanalysis_code,
    "unitanalysis_name",
    CAST("dataelement_code" AS BIGINT) AS dataelement_code,
    "dataelement_name",
    "sizeclass_code",
    "sizeclass_name",
    "dataclass_code",
    "dataclass_name",
    "ratelevel_code",
    "ratelevel_name",
    "periodicity_code",
    "periodicity_name",
    CAST("ownership_code" AS BIGINT) AS ownership_code,
    "ownership_name",
    "series_title"
FROM "bls-bd"
