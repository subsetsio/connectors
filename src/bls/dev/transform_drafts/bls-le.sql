-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `period` mixes regular observations with BLS aggregate period codes — Q05 (annual average). `period_start_date` is derived as the first day of the observation period, so an aggregate row lands on the same date as the year's first regular row (M13/S01/S03/A01 and Q05 all stamp January 1). Filter on `period` — grouping or summing by `period_start_date` alone double-counts.
-- caution: A single table holds quarterly (Q01-Q04) and annual (A01) observations; `period` is the only column that tells them apart.
-- caution: Carries both seasonally adjusted (`seasonal` = 'S') and unadjusted ('U') versions of the same underlying series; filter `seasonal` or you will mix two measurements of the same quantity.
-- caution: `value` is untyped across rows: what it measures is selected by `tdata_code`, `earn_code` and `pcts_code` (levels vs earnings vs percentages). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: Demographic dimension codes carry 'all'/'total' rows alongside their breakdowns; crossing them and summing double-counts the same people.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    CAST("lfst_code" AS BIGINT) AS lfst_code,
    "lfst_name",
    "fips_code",
    "fips_name",
    "series_title",
    "tdata_code",
    "tdata_name",
    "pcts_code",
    "pcts_name",
    "earn_code",
    "earn_name",
    "cert_code",
    "cert_name",
    "class_code",
    "class_name",
    CAST("unin_code" AS BIGINT) AS unin_code,
    "unin_name",
    "indy_code",
    "indy_name",
    "occupation_code",
    "occupation_name",
    "education_code",
    "education_name",
    "ages_code",
    "ages_name",
    "race_code",
    "race_name",
    "orig_code",
    "orig_name",
    CAST("sexs_code" AS BIGINT) AS sexs_code,
    "sexs_name",
    "born_code",
    "born_name",
    "seasonal",
    "seasonal_name"
FROM "bls-le"
