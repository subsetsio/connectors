-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Owner_Occupied" AS total_owner_occupied,
    "Total_Rented" AS total_rented,
    "Total_Others" AS total_others,
    "1Person_Total" AS 1person_total,
    "1Person_Owner_Occupied" AS 1person_owner_occupied,
    "1Person_Rented" AS 1person_rented,
    "1Person_Others" AS 1person_others,
    "2Persons_Total" AS 2persons_total,
    "2Persons_Owner_Occupied" AS 2persons_owner_occupied,
    "2Persons_Rented" AS 2persons_rented,
    "2Persons_Others" AS 2persons_others,
    "3Persons_Total" AS 3persons_total,
    "3Persons_Owner_Occupied" AS 3persons_owner_occupied,
    "3Persons_Rented" AS 3persons_rented,
    "3Persons_Others" AS 3persons_others,
    "4Persons_Total" AS 4persons_total,
    "4Persons_Owner_Occupied" AS 4persons_owner_occupied,
    "4Persons_Rented" AS 4persons_rented,
    "4Persons_Others" AS 4persons_others,
    "5Persons_Total" AS 5persons_total,
    "5Persons_Owner_Occupied" AS 5persons_owner_occupied,
    "5Persons_Rented" AS 5persons_rented,
    "5Persons_Others" AS 5persons_others,
    "6orMorePersons_Total" AS 6ormorepersons_total,
    "6orMorePersons_Owner_Occupied" AS 6ormorepersons_owner_occupied,
    "6orMorePersons_Rented" AS 6ormorepersons_rented,
    "6orMorePersons_Others" AS 6ormorepersons_others
FROM "sg-data-d-477f87b373df8660ee05d9e82d5f4bcf"
