-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Responses are already aggregated by country, region, variable, and response category; filter to a single variable/response before comparing countries.
SELECT
    "region",
    "country_code",
    "country",
    "response",
    "freq",
    "N" AS n,
    "prop",
    "pct",
    "variable",
    "_source_file" AS source_file
FROM "meta-climate-change-opinion-survey"
