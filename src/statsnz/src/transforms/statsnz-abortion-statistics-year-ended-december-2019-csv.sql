-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("Period" AS BIGINT) AS period,
    CAST("General_abortion_rate" AS DOUBLE) AS general_abortion_rate,
    "Induced_abortions" AS induced_abortions,
    "Age_of_woman" AS age_of_woman,
    CAST("Abortion_rate" AS DOUBLE) AS abortion_rate,
    "column_4",
    "column_5",
    "column_6",
    "column_7",
    "column_8",
    "column_9",
    "column_10",
    "column_11",
    "column_12",
    "column_13"
FROM "statsnz-abortion-statistics-year-ended-december-2019-csv"
