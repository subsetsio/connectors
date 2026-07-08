SELECT
    CAST(date AS DATE) AS date,
    ofr_fsi, credit, equity_valuation, safe_assets, funding,
    volatility, united_states, other_advanced_economies, emerging_markets
FROM "ofr-fsi"
WHERE date IS NOT NULL
ORDER BY date
