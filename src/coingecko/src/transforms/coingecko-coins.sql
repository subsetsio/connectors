SELECT id AS coin_id, symbol, name
FROM "coingecko-coins"
WHERE id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY id ORDER BY name) = 1
