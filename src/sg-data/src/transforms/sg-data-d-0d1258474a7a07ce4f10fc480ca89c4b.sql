-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Ambulant_Total" AS ambulant_total,
    "Ambulant_Males" AS ambulant_males,
    "Ambulant_Females" AS ambulant_females,
    "Semi_Ambulant_Total" AS semi_ambulant_total,
    "Semi_Ambulant_Males" AS semi_ambulant_males,
    "Semi_Ambulant_Females" AS semi_ambulant_females,
    "Non_Ambulant_Total" AS non_ambulant_total,
    "Non_Ambulant_Males" AS non_ambulant_males,
    "Non_Ambulant_Females" AS non_ambulant_females
FROM "sg-data-d-0d1258474a7a07ce4f10fc480ca89c4b"
