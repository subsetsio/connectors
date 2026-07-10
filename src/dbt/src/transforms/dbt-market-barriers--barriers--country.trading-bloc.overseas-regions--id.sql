-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "barriers__id" AS barriers_id,
    "country.trading_bloc.overseas_regions__id" AS country_trading_bloc_overseas_regions_id
FROM "dbt-market-barriers--barriers--country.trading-bloc.overseas-regions--id"
