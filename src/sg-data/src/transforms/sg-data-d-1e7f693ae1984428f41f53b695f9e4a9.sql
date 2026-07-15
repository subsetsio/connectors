-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Upto15mins_Total" AS upto15mins_total,
    "Upto15mins_Males" AS upto15mins_males,
    "Upto15mins_Females" AS upto15mins_females,
    "16_30mins_Total" AS 16_30mins_total,
    "16_30mins_Males" AS 16_30mins_males,
    "16_30mins_Females" AS 16_30mins_females,
    "31_45mins_Total" AS 31_45mins_total,
    "31_45mins_Males" AS 31_45mins_males,
    "31_45mins_Females" AS 31_45mins_females,
    "46_60mins_Total" AS 46_60mins_total,
    "46_60mins_Males" AS 46_60mins_males,
    "46_60mins_Females" AS 46_60mins_females,
    "Morethan60mins_Total" AS morethan60mins_total,
    "Morethan60mins_Males" AS morethan60mins_males,
    "Morethan60mins_Females" AS morethan60mins_females
FROM "sg-data-d-1e7f693ae1984428f41f53b695f9e4a9"
