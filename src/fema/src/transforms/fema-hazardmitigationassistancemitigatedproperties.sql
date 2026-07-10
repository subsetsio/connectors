-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "propertyPartOfProject" AS propertypartofproject,
    "region",
    CAST("stateNumberCode" AS BIGINT) AS statenumbercode,
    "state",
    "foundationType" AS foundationtype,
    "county",
    "city",
    "zip",
    "projectIdentifier" AS projectidentifier,
    "propertyAction" AS propertyaction,
    "structureType" AS structuretype,
    "typeOfResidency" AS typeofresidency,
    "actualAmountPaid" AS actualamountpaid,
    "programFy" AS programfy,
    "programArea" AS programarea,
    "numberOfProperties" AS numberofproperties,
    "damageCategory" AS damagecategory
FROM "fema-hazardmitigationassistancemitigatedproperties"
