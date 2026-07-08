SELECT
    date,
    question_code,
    question_text,
    answer_code,
    answer_label,
    respondent_count,
    total_per_question,
    percent
FROM "nfib-survey-responses"
ORDER BY question_code, date, answer_code
