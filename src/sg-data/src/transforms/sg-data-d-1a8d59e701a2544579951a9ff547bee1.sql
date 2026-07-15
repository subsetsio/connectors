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
    "Below_1_000_Total" AS below_1_000_total,
    "Below_1_000_Males" AS below_1_000_males,
    "Below_1_000_Females" AS below_1_000_females,
    "1_000_1_999_Total" AS 1_000_1_999_total,
    "1_000_1_999_Males" AS 1_000_1_999_males,
    "1_000_1_999_Females" AS 1_000_1_999_females,
    "2_000_2_999_Total" AS 2_000_2_999_total,
    "2_000_2_999_Males" AS 2_000_2_999_males,
    "2_000_2_999_Females" AS 2_000_2_999_females,
    "3_000_3_999_Total" AS 3_000_3_999_total,
    "3_000_3_999_Males" AS 3_000_3_999_males,
    "3_000_3_999_Females" AS 3_000_3_999_females,
    "4_000_4_999_Total" AS 4_000_4_999_total,
    "4_000_4_999_Males" AS 4_000_4_999_males,
    "4_000_4_999_Females" AS 4_000_4_999_females,
    "5_000_5_999_Total" AS 5_000_5_999_total,
    "5_000_5_999_Males" AS 5_000_5_999_males,
    "5_000_5_999_Females" AS 5_000_5_999_females,
    "6_000_6_999_Total" AS 6_000_6_999_total,
    "6_000_6_999_Males" AS 6_000_6_999_males,
    "6_000_6_999_Females" AS 6_000_6_999_females,
    "7_000_7_999_Total" AS 7_000_7_999_total,
    "7_000_7_999_Males" AS 7_000_7_999_males,
    "7_000_7_999_Females" AS 7_000_7_999_females,
    "8_000andOver_Total" AS 8_000andover_total,
    "8_000andOver_Males" AS 8_000andover_males,
    "8_000andOver_Females" AS 8_000andover_females
FROM "sg-data-d-1a8d59e701a2544579951a9ff547bee1"
