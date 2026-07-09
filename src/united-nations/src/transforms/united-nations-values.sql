-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix countries, territories, regions and aggregate geographic areas, so filter geo_area_code against the geoareas taxonomy before aggregating.
-- caution: The table mixes many SDG series, units and disaggregation definitions; filter by series_code and dimensions before comparing or summing values.
-- caution: The raw values export does not provide a scan-verified row key; duplicate source rows can exist across the apparent observation tuple.
SELECT
    CAST("goal" AS BIGINT) AS goal,
    "target",
    "indicator",
    "series_code",
    "series_description",
    CAST("geo_area_code" AS BIGINT) AS geo_area_code,
    "geo_area_name",
    CAST("time_period" AS BIGINT) AS time_period,
    "value",
    "time_detail",
    "time_coverage",
    "upper_bound",
    "lower_bound",
    "base_period",
    "source",
    "geo_info_url",
    "footnote",
    "units",
    "nature",
    "dimensions"
FROM "united-nations-values"
