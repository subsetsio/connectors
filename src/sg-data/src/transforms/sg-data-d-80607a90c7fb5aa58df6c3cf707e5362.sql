-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Homemakers_Total" AS homemakers_total,
    "Homemakers_Males" AS homemakers_males,
    "Homemakers_Females" AS homemakers_females,
    "Retired_Total" AS retired_total,
    "Retired_Males" AS retired_males,
    "Retired_Females" AS retired_females,
    "Students_Total" AS students_total,
    "Students_Males" AS students_males,
    "Students_Females" AS students_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-80607a90c7fb5aa58df6c3cf707e5362"
