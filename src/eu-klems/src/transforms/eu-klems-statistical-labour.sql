-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country column includes multi-country aggregates such as EU and euro-area totals alongside individual countries; filter it before summing across economies.
-- caution: Rows combine multiple industries and labour demographic breakdowns; aggregate only after filtering or grouping by the relevant industry, gender, age, education, and variable dimensions.
SELECT
    "country",
    "var",
    "code",
    CAST("Sort_ID" AS BIGINT) AS sort_id,
    "indnr",
    CAST("gender" AS BIGINT) AS gender,
    CAST("age" AS BIGINT) AS age,
    CAST("edu" AS BIGINT) AS edu,
    "year",
    "value"
FROM "eu-klems-statistical-labour"
