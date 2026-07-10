SELECT
    variable_code,
    CAST(question_id AS BIGINT) AS question_id,
    question_title,
    section,
    country,
    CAST(round_num AS INTEGER) AS round_num,
    round_label,
    CAST(answer_code AS INTEGER) AS answer_code,
    answer_label,
    is_missing,
    CAST(weighted_n AS DOUBLE) AS weighted_n,
    CAST(pct_valid AS DOUBLE) AS pct_valid
FROM "afrobarometer-values"
WHERE pct_valid IS NOT NULL
  AND variable_code IS NOT NULL
  AND country IS NOT NULL
  AND round_num IS NOT NULL
  AND answer_code IS NOT NULL
