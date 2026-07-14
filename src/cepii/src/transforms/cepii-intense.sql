-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are directional actor-pair category observations; reverse directions are distinct.
SELECT
    "Date" AS date,
    "Actor1CountryCode" AS actor1countrycode,
    "Actor2CountryCode" AS actor2countrycode,
    "Category" AS category,
    "NumEvents" AS numevents,
    "NumArticles" AS numarticles,
    "Shade" AS shade,
    "Intensity" AS intensity
FROM "cepii-intense"
