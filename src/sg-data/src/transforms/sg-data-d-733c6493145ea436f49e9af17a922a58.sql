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
    "NumberOfHoursWorked_Below30_Total" AS numberofhoursworked_below30_total,
    "NumberOfHoursWorked_Below30_Males" AS numberofhoursworked_below30_males,
    "NumberOfHoursWorked_Below30_Females" AS numberofhoursworked_below30_females,
    "NumberOfHoursWorked_30_34_Total" AS numberofhoursworked_30_34_total,
    "NumberOfHoursWorked_30_34_Males" AS numberofhoursworked_30_34_males,
    "NumberOfHoursWorked_30_34_Females" AS numberofhoursworked_30_34_females,
    "NumberOfHoursWorked_35_39_Total" AS numberofhoursworked_35_39_total,
    "NumberOfHoursWorked_35_39_Males" AS numberofhoursworked_35_39_males,
    "NumberOfHoursWorked_35_39_Females" AS numberofhoursworked_35_39_females,
    "NumberOfHoursWorked_40_44_Total" AS numberofhoursworked_40_44_total,
    "NumberOfHoursWorked_40_44_Males" AS numberofhoursworked_40_44_males,
    "NumberOfHoursWorked_40_44_Females" AS numberofhoursworked_40_44_females,
    "NumberOfHoursWorked_45_49_Total" AS numberofhoursworked_45_49_total,
    "NumberOfHoursWorked_45_49_Males" AS numberofhoursworked_45_49_males,
    "NumberOfHoursWorked_45_49_Females" AS numberofhoursworked_45_49_females,
    "NumberOfHoursWorked_50_54_Total" AS numberofhoursworked_50_54_total,
    "NumberOfHoursWorked_50_54_Males" AS numberofhoursworked_50_54_males,
    "NumberOfHoursWorked_50_54_Females" AS numberofhoursworked_50_54_females,
    "NumberOfHoursWorked_55_59_Total" AS numberofhoursworked_55_59_total,
    "NumberOfHoursWorked_55_59_Males" AS numberofhoursworked_55_59_males,
    "NumberOfHoursWorked_55_59_Females" AS numberofhoursworked_55_59_females,
    "NumberOfHoursWorked_60_64_Total" AS numberofhoursworked_60_64_total,
    "NumberOfHoursWorked_60_64_Males" AS numberofhoursworked_60_64_males,
    "NumberOfHoursWorked_60_64_Females" AS numberofhoursworked_60_64_females,
    "NumberOfHoursWorked_65andOver_Total" AS numberofhoursworked_65andover_total,
    "NumberOfHoursWorked_65andOver_Males" AS numberofhoursworked_65andover_males,
    "NumberOfHoursWorked_65andOver_Females" AS numberofhoursworked_65andover_females
FROM "sg-data-d-733c6493145ea436f49e9af17a922a58"
