-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains SDG observations across many series, geographies, units implicit in the series, and source revisions; filter to a single series and compatible geography level before comparing values.
SELECT
    "series",
    "series_description",
    "goal",
    "target",
    "indicator",
    "geo_area_code",
    "geo_area_name",
    "time_period",
    TRY_CAST("value" AS DOUBLE) AS value,
    "value_type",
    "source"
FROM "un-statistics-division-sdg-data"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
