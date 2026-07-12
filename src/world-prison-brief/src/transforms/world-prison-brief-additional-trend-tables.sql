-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows come from multiple additional trend table layouts; use table_title and headers to distinguish female prisoner and pre-trial/remand measures before comparing values.
SELECT
    "jurisdiction_id",
    "jurisdiction_name",
    "region",
    "table_title",
    "headers",
    "column_1" AS year_text,
    "column_2" AS count_text,
    "column_3" AS percent_of_total_prison_population_text,
    "column_4" AS population_rate_per_100k_text,
    "country_url"
FROM "world-prison-brief-additional-trend-tables"
