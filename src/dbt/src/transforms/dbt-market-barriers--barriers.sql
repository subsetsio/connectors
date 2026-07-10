-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "title",
    "summary",
    "is_resolved",
    "status_date",
    "country_or_territory_name",
    "country_or_territory_trading_bloc",
    "caused_by_trading_bloc",
    "trading_bloc",
    "location",
    "sectors",
    "last_published_on",
    "reported_on"
FROM "dbt-market-barriers--barriers"
