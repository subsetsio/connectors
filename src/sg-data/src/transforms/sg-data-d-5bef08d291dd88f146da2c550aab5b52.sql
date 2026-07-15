-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Before1971_Total" AS before1971_total,
    "Before1971_Males" AS before1971_males,
    "Before1971_Females" AS before1971_females,
    "1971_1980_Total" AS 1971_1980_total,
    "1971_1980_Males" AS 1971_1980_males,
    "1971_1980_Females" AS 1971_1980_females,
    "1981_1990_Total" AS 1981_1990_total,
    "1981_1990_Males" AS 1981_1990_males,
    "1981_1990_Females" AS 1981_1990_females,
    "1991_2000_Total" AS 1991_2000_total,
    "1991_2000_Males" AS 1991_2000_males,
    "1991_2000_Females" AS 1991_2000_females
FROM "sg-data-d-5bef08d291dd88f146da2c550aab5b52"
