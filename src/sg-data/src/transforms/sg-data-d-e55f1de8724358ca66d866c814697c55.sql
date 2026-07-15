-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "DurationInPresentJob_LessThan1Year_Total" AS durationinpresentjob_lessthan1year_total,
    "DurationInPresentJob_LessThan1Year_Males" AS durationinpresentjob_lessthan1year_males,
    "DurationInPresentJob_LessThan1Year_Females" AS durationinpresentjob_lessthan1year_females,
    "DurationInPresentJob_1Year_Total" AS durationinpresentjob_1year_total,
    "DurationInPresentJob_1Year_Males" AS durationinpresentjob_1year_males,
    "DurationInPresentJob_1Year_Females" AS durationinpresentjob_1year_females,
    "DurationInPresentJob_2_3Years_Total" AS durationinpresentjob_2_3years_total,
    "DurationInPresentJob_2_3Years_Males" AS durationinpresentjob_2_3years_males,
    "DurationInPresentJob_2_3Years_Females" AS durationinpresentjob_2_3years_females,
    "DurationInPresentJob_4_5Years_Total" AS durationinpresentjob_4_5years_total,
    "DurationInPresentJob_4_5Years_Males" AS durationinpresentjob_4_5years_males,
    "DurationInPresentJob_4_5Years_Females" AS durationinpresentjob_4_5years_females,
    "DurationInPresentJob_6_10Years_Total" AS durationinpresentjob_6_10years_total,
    "DurationInPresentJob_6_10Years_Males" AS durationinpresentjob_6_10years_males,
    "DurationInPresentJob_6_10Years_Females" AS durationinpresentjob_6_10years_females,
    "DurationInPresentJob_11_15Years_Total" AS durationinpresentjob_11_15years_total,
    "DurationInPresentJob_11_15Years_Males" AS durationinpresentjob_11_15years_males,
    "DurationInPresentJob_11_15Years_Females" AS durationinpresentjob_11_15years_females,
    "DurationInPresentJob_MoreThan15Years_Total" AS durationinpresentjob_morethan15years_total,
    "DurationInPresentJob_MoreThan15Years_Males" AS durationinpresentjob_morethan15years_males,
    "DurationInPresentJob_MoreThan15Years_Females" AS durationinpresentjob_morethan15years_females
FROM "sg-data-d-e55f1de8724358ca66d866c814697c55"
