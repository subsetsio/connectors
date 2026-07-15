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
    "Below30_Total" AS below30_total,
    "Below30_Males" AS below30_males,
    "Below30_Females" AS below30_females,
    "30_34_Total" AS 30_34_total,
    "30_34_Males" AS 30_34_males,
    "30_34_Females" AS 30_34_females,
    "35_39_Total" AS 35_39_total,
    "35_39_Males" AS 35_39_males,
    "35_39_Females" AS 35_39_females,
    "40_44_Total" AS 40_44_total,
    "40_44_Males" AS 40_44_males,
    "40_44_Females" AS 40_44_females,
    "45_49_Total" AS 45_49_total,
    "45_49_Males" AS 45_49_males,
    "45_49_Females" AS 45_49_females,
    "50_54_Total" AS 50_54_total,
    "50_54_Males" AS 50_54_males,
    "50_54_Females" AS 50_54_females,
    "55_59_Total" AS 55_59_total,
    "55_59_Males" AS 55_59_males,
    "55_59_Females" AS 55_59_females,
    "60_64_Total" AS 60_64_total,
    "60_64_Males" AS 60_64_males,
    "60_64_Females" AS 60_64_females,
    "65andOver_Total" AS 65andover_total,
    "65andOver_Males" AS 65andover_males,
    "65andOver_Females" AS 65andover_females
FROM "sg-data-d-91b6d195dfb9bbe4836687b686fb4987"
