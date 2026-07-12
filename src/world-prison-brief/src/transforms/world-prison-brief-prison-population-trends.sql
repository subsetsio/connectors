-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The two measures in each row are separate historical series for the same jurisdiction and date: total prison population and prison population rate.
SELECT
    "jurisdiction_id",
    "jurisdiction_name",
    "region",
    strptime("observation_date", '%Y-%m-%d')::DATE AS observation_date,
    CAST("year_text" AS BIGINT) AS year_text,
    "prison_population_total_text",
    "prison_population_rate_text",
    "country_url"
FROM "world-prison-brief-prison-population-trends"
