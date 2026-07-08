SELECT
    CAST(date AS DATE)                  AS date,
    CAST(bullish AS DOUBLE)             AS bullish,
    CAST(neutral AS DOUBLE)             AS neutral,
    CAST(bearish AS DOUBLE)             AS bearish,
    CAST(total AS DOUBLE)               AS total,
    CAST(bullish_8wk_mov_avg AS DOUBLE) AS bullish_8wk_mov_avg,
    CAST(bull_bear_spread AS DOUBLE)    AS bull_bear_spread,
    CAST(bullish_average AS DOUBLE)     AS bullish_average,
    CAST(bullish_avg_plus_stdev AS DOUBLE)  AS bullish_avg_plus_stdev,
    CAST(bullish_avg_minus_stdev AS DOUBLE) AS bullish_avg_minus_stdev,
    CAST(sp500_weekly_high AS DOUBLE)   AS sp500_weekly_high,
    CAST(sp500_weekly_low AS DOUBLE)    AS sp500_weekly_low,
    CAST(sp500_weekly_close AS DOUBLE)  AS sp500_weekly_close
FROM "aaii-investor-sentiment-survey-investor-sentiment-survey-weekly"
WHERE date IS NOT NULL
