-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("Period" AS BIGINT) AS period,
    "General Marriage_Rate_and Divorce_Rate" AS general_marriage_rate_and_divorce_rate,
    CAST("Count" AS DOUBLE) AS count,
    "Marriages_or_Divorces" AS marriages_or_divorces,
    "Same-Sex_or_Opposite_Sex" AS same_sex_or_opposite_sex,
    "Marriage_or_Civil_Union" AS marriage_or_civil_union,
    "Male_or_Female" AS male_or_female,
    CAST("Median_age_at _divorce" AS DOUBLE) AS median_age_at_divorce,
    "Status_before_Marriage" AS status_before_marriage,
    CAST("Median_Age_at_Marriage" AS DOUBLE) AS median_age_at_marriage
FROM "statsnz-marriages-civil-unions-and-divorces-year-ended-december-2020-csv"
