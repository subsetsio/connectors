-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `geo` includes countries plus regional and income aggregates; filter geography level before aggregating across geographies.
-- caution: The table excludes multidimensional datapoints with extra dimensions such as gender or age.
SELECT
    "repo",
    "geo_dim",
    "geo",
    CAST("time" AS BIGINT) AS time,
    "indicator",
    "value"
FROM "gapminder-values"
