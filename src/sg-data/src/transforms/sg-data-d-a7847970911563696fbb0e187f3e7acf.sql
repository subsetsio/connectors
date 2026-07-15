-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "UpTo15Mins_Total" AS upto15mins_total,
    "UpTo15Mins_Males" AS upto15mins_males,
    "UpTo15Mins_Females" AS upto15mins_females,
    "16_30Mins_Total" AS 16_30mins_total,
    "16_30Mins_Males" AS 16_30mins_males,
    "16_30Mins_Females" AS 16_30mins_females,
    "31_45Mins_Total" AS 31_45mins_total,
    "31_45Mins_Males" AS 31_45mins_males,
    "31_45Mins_Females" AS 31_45mins_females,
    "46_60Mins_Total" AS 46_60mins_total,
    "46_60Mins_Males" AS 46_60mins_males,
    "46_60Mins_Females" AS 46_60mins_females,
    "MoreThan60Mins_Total" AS morethan60mins_total,
    "MoreThan60Mins_Males" AS morethan60mins_males,
    "MoreThan60Mins_Females" AS morethan60mins_females
FROM "sg-data-d-a7847970911563696fbb0e187f3e7acf"
