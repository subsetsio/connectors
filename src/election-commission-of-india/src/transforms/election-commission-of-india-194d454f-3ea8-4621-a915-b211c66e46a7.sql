SELECT
    TRY_CAST("_sl__no_" AS BIGINT)        AS sl_no,
    CAST(state AS VARCHAR)                AS state,
    TRY_CAST(const_no_ AS BIGINT)         AS constituency_no,
    CAST(constituency AS VARCHAR)         AS constituency,
    CAST(constituency_type AS VARCHAR)    AS constituency_type,
    TRY_CAST(total_valid_votes AS BIGINT) AS total_valid_votes,
    CAST(winner_name AS VARCHAR)          AS winner_name,
    CAST(social_category AS VARCHAR)      AS winner_social_category,
    CAST(gender AS VARCHAR)               AS winner_gender,
    CAST(party AS VARCHAR)                AS winner_party,
    CAST(party_symbol AS VARCHAR)         AS winner_party_symbol,
    TRY_CAST(vote_secured AS BIGINT)      AS winner_vote_secured,
    CAST(runner_up_name AS VARCHAR)       AS runner_up_name,
    TRY_CAST(margin AS BIGINT)            AS margin,
    TRY_CAST(margin__ AS DOUBLE)          AS margin_pct
FROM "election-commission-of-india-194d454f-3ea8-4621-a915-b211c66e46a7"
WHERE winner_name IS NOT NULL
