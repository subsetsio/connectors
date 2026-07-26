-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "sheet_name",
    "row_number",
    "TERRITORY" AS territory,
    "Unnamed: 1" AS unnamed_1,
    "SCHOOL" AS school,
    "US TERRITORY" AS us_territory,
    "STATE" AS state,
    "CITY" AS city,
    "Unnamed: 0" AS unnamed_0,
    "LA" AS la,
    "201 Airport Drive" AS 201_airport_drive,
    "North Caddo Magnet High School" AS north_caddo_magnet_high_school,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "State_1" AS state_1,
    "City_1" AS city_1,
    "School_1" AS school_1
FROM "u-s-department-of-education-2015-awards-presidents-education-awards-program"
