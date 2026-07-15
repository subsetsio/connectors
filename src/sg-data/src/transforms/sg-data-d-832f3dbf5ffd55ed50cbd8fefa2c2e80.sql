-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PerCent" AS percent,
    "Total" AS total,
    "HouseholdSize_Persons_1" AS householdsize_persons_1,
    "HouseholdSize_Persons_2" AS householdsize_persons_2,
    "HouseholdSize_Persons_3" AS householdsize_persons_3,
    "HouseholdSize_Persons_4" AS householdsize_persons_4,
    "HouseholdSize_Persons_5" AS householdsize_persons_5,
    "HouseholdSize_Persons_6orMore" AS householdsize_persons_6ormore,
    "AverageHouseholdSize_Persons" AS averagehouseholdsize_persons
FROM "sg-data-d-832f3dbf5ffd55ed50cbd8fefa2c2e80"
