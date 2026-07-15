-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Owner" AS total_owner,
    "Total_Non_Owner" AS total_non_owner,
    "1Person_Total" AS 1person_total,
    "1Person_Owner" AS 1person_owner,
    "1Person_Non_Owner" AS 1person_non_owner,
    "2Persons_Total" AS 2persons_total,
    "2Persons_Owner" AS 2persons_owner,
    "2Persons_Non_Owner" AS 2persons_non_owner,
    "3Persons_Total" AS 3persons_total,
    "3Persons_Owner" AS 3persons_owner,
    "3Persons_Non_Owner" AS 3persons_non_owner,
    "4Persons_Total" AS 4persons_total,
    "4Persons_Owner" AS 4persons_owner,
    "4Persons_Non_Owner" AS 4persons_non_owner,
    "5Persons_Total" AS 5persons_total,
    "5Persons_Owner" AS 5persons_owner,
    "5Persons_Non_Owner" AS 5persons_non_owner,
    "6OrMorePersons_Total" AS 6ormorepersons_total,
    "6OrMorePersons_Owner" AS 6ormorepersons_owner,
    "6OrMorePersons_Non_Owner" AS 6ormorepersons_non_owner
FROM "sg-data-d-04053a34970c8d8d5c5a695028b0799c"
