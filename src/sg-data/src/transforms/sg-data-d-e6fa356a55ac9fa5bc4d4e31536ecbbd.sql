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
    "Before1941_Total" AS before1941_total,
    "Before1941_Males" AS before1941_males,
    "Before1941_Females" AS before1941_females,
    "1941_1950_Total" AS 1941_1950_total,
    "1941_1950_Males" AS 1941_1950_males,
    "1941_1950_Females" AS 1941_1950_females,
    "1951_1960_Total" AS 1951_1960_total,
    "1951_1960_Males" AS 1951_1960_males,
    "1951_1960_Females" AS 1951_1960_females,
    "1961_1970_Total" AS 1961_1970_total,
    "1961_1970_Males" AS 1961_1970_males,
    "1961_1970_Females" AS 1961_1970_females,
    "1971_1980_Total" AS 1971_1980_total,
    "1971_1980_Males" AS 1971_1980_males,
    "1971_1980_Females" AS 1971_1980_females,
    "1981_1990_Total" AS 1981_1990_total,
    "1981_1990_Males" AS 1981_1990_males,
    "1981_1990_Females" AS 1981_1990_females,
    "1991_2000_Total" AS 1991_2000_total,
    "1991_2000_Males" AS 1991_2000_males,
    "1991_2000_Females" AS 1991_2000_females
FROM "sg-data-d-e6fa356a55ac9fa5bc4d4e31536ecbbd"
