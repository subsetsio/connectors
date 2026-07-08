SELECT
    active_cryptocurrencies,
    upcoming_icos,
    ongoing_icos,
    ended_icos,
    markets,
    total_market_cap_usd,
    total_volume_usd,
    market_cap_percentage_btc,
    market_cap_percentage_eth,
    market_cap_change_percentage_24h_usd,
    CAST(to_timestamp(updated_at) AS TIMESTAMP) AS updated_at
FROM "coingecko-global"
