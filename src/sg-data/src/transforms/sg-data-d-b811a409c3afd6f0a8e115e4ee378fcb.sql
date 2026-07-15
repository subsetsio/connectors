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
    "Below30Hours_Total" AS below30hours_total,
    "Below30Hours_Males" AS below30hours_males,
    "Below30Hours_Females" AS below30hours_females,
    "30_34Hours_Total" AS 30_34hours_total,
    "30_34Hours_Males" AS 30_34hours_males,
    "30_34Hours_Females" AS 30_34hours_females,
    "35_39Hours_Total" AS 35_39hours_total,
    "35_39Hours_Males" AS 35_39hours_males,
    "35_39Hours_Females" AS 35_39hours_females,
    "40_44Hours_Total" AS 40_44hours_total,
    "40_44Hours_Males" AS 40_44hours_males,
    "40_44Hours_Females" AS 40_44hours_females,
    "45_49Hours_Total" AS 45_49hours_total,
    "45_49Hours_Males" AS 45_49hours_males,
    "45_49Hours_Females" AS 45_49hours_females,
    "50_54Hours_Total" AS 50_54hours_total,
    "50_54Hours_Males" AS 50_54hours_males,
    "50_54Hours_Females" AS 50_54hours_females,
    "55_59Hours_Total" AS 55_59hours_total,
    "55_59Hours_Males" AS 55_59hours_males,
    "55_59Hours_Females" AS 55_59hours_females,
    "60_64Hours_Total" AS 60_64hours_total,
    "60_64Hours_Males" AS 60_64hours_males,
    "60_64Hours_Females" AS 60_64hours_females,
    "65HoursandOver_Total" AS 65hoursandover_total,
    "65HoursandOver_Males" AS 65hoursandover_males,
    "65HoursandOver_Females" AS 65hoursandover_females
FROM "sg-data-d-b811a409c3afd6f0a8e115e4ee378fcb"
