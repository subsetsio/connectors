-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Before1991_Total" AS before1991_total,
    "Before1991_Males" AS before1991_males,
    "Before1991_Females" AS before1991_females,
    "1991_1995_Total" AS 1991_1995_total,
    "1991_1995_Males" AS 1991_1995_males,
    "1991_1995_Females" AS 1991_1995_females,
    "1996_2000_Total" AS 1996_2000_total,
    "1996_2000_Males" AS 1996_2000_males,
    "1996_2000_Females" AS 1996_2000_females,
    "2001_2005_Total" AS 2001_2005_total,
    "2001_2005_Males" AS 2001_2005_males,
    "2001_2005_Females" AS 2001_2005_females
FROM "sg-data-d-179db63b1723312480203eecadb072e4"
