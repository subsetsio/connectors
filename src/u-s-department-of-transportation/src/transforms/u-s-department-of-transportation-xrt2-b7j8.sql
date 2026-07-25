-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("number_of_aircraft" AS BIGINT) AS number_of_aircraft,
    CAST("average_year_of_manufacture" AS DOUBLE) AS average_year_of_manufacture,
    CAST("oldest_year_of_manufacture" AS BIGINT) AS oldest_year_of_manufacture,
    CAST("youngest_year_of_manufacture" AS BIGINT) AS youngest_year_of_manufacture,
    CAST("average_age" AS DOUBLE) AS average_age,
    CAST("oldest_age" AS BIGINT) AS oldest_age,
    CAST("youngest_age" AS BIGINT) AS youngest_age
FROM "u-s-department-of-transportation-xrt2-b7j8"
