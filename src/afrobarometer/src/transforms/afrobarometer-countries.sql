SELECT
    country,
    CAST(region_id AS BIGINT) AS region_id,
    mpcod,
    CAST(valor AS BIGINT) AS valor,
    round_nums,
    CAST(n_rounds AS INTEGER) AS n_rounds,
    CAST(first_round_num AS INTEGER) AS first_round_num,
    CAST(latest_round_num AS INTEGER) AS latest_round_num
FROM "afrobarometer-countries"
WHERE country IS NOT NULL
