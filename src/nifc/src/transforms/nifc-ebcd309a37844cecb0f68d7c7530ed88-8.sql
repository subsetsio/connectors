-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "Department" AS department,
    "Agency" AS agency,
    "Unit" AS unit,
    "UnitID" AS unitid,
    "OrgCode" AS orgcode,
    "Region" AS region,
    "CostCenterCode" AS costcentercode,
    "OrgType" AS orgtype,
    "RegionCode" AS regioncode,
    "FireManagementGroup" AS firemanagementgroup,
    "UnitCode" AS unitcode,
    "SubUnit" AS subunit,
    "UnitType" AS unittype,
    "RegionalUnit" AS regionalunit,
    "TribeName" AS tribename,
    "TribeFullName" AS tribefullname,
    "GlobalID" AS globalid,
    "ID" AS id
FROM "nifc-ebcd309a37844cecb0f68d7c7530ed88-8"
