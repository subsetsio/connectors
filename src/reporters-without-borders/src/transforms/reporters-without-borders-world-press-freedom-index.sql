SELECT
    iso,
    country,
    CAST(year AS INTEGER)              AS year,
    CAST(score AS DOUBLE)              AS score,
    CAST(rank AS INTEGER)              AS rank,
    zone,
    political_context,
    rank_pol,
    economic_context,
    rank_eco,
    legal_context,
    rank_leg,
    social_context,
    rank_soc,
    safety,
    rank_saf,
    rank_prev,
    rank_evolution,
    score_prev,
    score_evolution,
    methodology_era,
    score_scale
FROM "reporters-without-borders-world-press-freedom-index"
WHERE iso IS NOT NULL
  AND year IS NOT NULL
  AND score IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY iso, year ORDER BY score DESC) = 1
