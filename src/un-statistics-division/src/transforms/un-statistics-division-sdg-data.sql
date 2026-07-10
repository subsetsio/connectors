-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains SDG observations across many series, geographies, units implicit in the series, and source revisions; filter to a single series and compatible geography level before comparing values.
SELECT
    "series",
    "series_description",
    CAST("goal" AS BIGINT) AS goal,
    "target",
    "indicator",
    CAST("geo_area_code" AS BIGINT) AS geo_area_code,
    "geo_area_name",
    "time_period",
    "value",
    "value_type",
    "source"
FROM "un-statistics-division-sdg-data"
