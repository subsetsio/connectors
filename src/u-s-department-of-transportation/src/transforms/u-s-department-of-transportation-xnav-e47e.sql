-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "airport",
    "code",
    CAST("passengers" AS BIGINT) AS passengers,
    "border",
    "port",
    CAST("person_crossings" AS BIGINT) AS person_crossings,
    CAST("border_year" AS BIGINT) AS border_year,
    CAST("airport_year" AS BIGINT) AS airport_year
FROM "u-s-department-of-transportation-xnav-e47e"
