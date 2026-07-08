SELECT
    fideid                                          AS fide_id,
    name,
    country                                         AS federation,
    sex,
    NULLIF(title, '')                               AS title,
    NULLIF(w_title, '')                             AS women_title,
    NULLIF(o_title, '')                             AS other_title,
    NULLIF(foa_title, '')                           AS foa_title,
    rating                                          AS standard_rating,
    games                                           AS standard_games,
    k                                               AS standard_k,
    rapid_rating,
    rapid_games,
    rapid_k,
    blitz_rating,
    blitz_games,
    blitz_k,
    CASE WHEN birthday > 0 THEN birthday END        AS birth_year,
    NULLIF(flag, '')                                AS inactive_flag
FROM "fide-players"
WHERE fideid IS NOT NULL
