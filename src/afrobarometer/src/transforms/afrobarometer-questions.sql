SELECT
    variable_code,
    CAST(question_id AS BIGINT) AS question_id,
    title,
    section,
    CAST(n_rounds AS INTEGER) AS n_rounds,
    round_nums,
    CAST(latest_round_num AS INTEGER) AS latest_round_num
FROM "afrobarometer-questions"
WHERE variable_code IS NOT NULL
