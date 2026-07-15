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
    "LessThan1Year_Total" AS lessthan1year_total,
    "LessThan1Year_Males" AS lessthan1year_males,
    "LessThan1Year_Females" AS lessthan1year_females,
    "1Year_Total" AS 1year_total,
    "1Year_Males" AS 1year_males,
    "1Year_Females" AS 1year_females,
    "2_3Years_Total" AS 2_3years_total,
    "2_3Years_Males" AS 2_3years_males,
    "2_3Years_Females" AS 2_3years_females,
    "4_5Years_Total" AS 4_5years_total,
    "4_5Years_Males" AS 4_5years_males,
    "4_5Years_Females" AS 4_5years_females,
    "6_10Years_Total" AS 6_10years_total,
    "6_10Years_Males" AS 6_10years_males,
    "6_10Years_Females" AS 6_10years_females,
    "11_15Years_Total" AS 11_15years_total,
    "11_15Years_Males" AS 11_15years_males,
    "11_15Years_Females" AS 11_15years_females,
    "MoreThan15Years_Total" AS morethan15years_total,
    "MoreThan15Years_Males" AS morethan15years_males,
    "MoreThan15Years_Females" AS morethan15years_females
FROM "sg-data-d-059f67b287fc325b141c9ce4aa01d694"
