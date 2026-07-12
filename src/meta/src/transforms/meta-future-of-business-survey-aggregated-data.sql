-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table unions multiple Future of Business survey extracts with different schemas and many file-specific identifier columns.
-- caution: Rows are pre-aggregated survey estimates; compare within a consistent source file, population, question, and answer coding.
SELECT
    "variable",
    "value",
    "pop",
    "logged_iso2",
    "mean_w",
    "se_w",
    "count",
    "question_n",
    "question_text",
    "_source_file" AS source_file,
    "country_iso2",
    "column0" AS source_row_number,
    "population",
    "Country" AS country,
    "Wave (number)" AS wave_number,
    "Wave (month/year)" AS wave_month_year,
    "Topic covered by question" AS topic_covered_by_question,
    "Question" AS question,
    "Question/Row number" AS question_row_number,
    "Row item label" AS row_item_label,
    "Answer option label" AS answer_option_label,
    "Base description (Who saw the question?)" AS base_description_who_saw_the_question,
    "Base size (How many saw this question?)" AS base_size_how_many_saw_this_question,
    "Data type represented by ""value""" AS data_type_represented_by_value
FROM "meta-future-of-business-survey-aggregated-data"
