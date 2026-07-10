-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Fire perimeter rows include incident identifiers and ArcGIS geometry measures; one incident can have related records in other wildfire-loss tables.
SELECT
    "OBJECTID" AS objectid,
    "YEAR_" AS year,
    "STATE" AS state,
    "AGENCY" AS agency,
    "UNIT_ID" AS unit_id,
    "FIRE_NAME" AS fire_name,
    "INC_NUM" AS inc_num,
    "ALARM_DATE" AS alarm_date,
    "CONT_DATE" AS cont_date,
    "CAUSE" AS cause,
    "C_METHOD" AS c_method,
    "OBJECTIVE" AS objective,
    "GIS_ACRES" AS gis_acres,
    "COMMENTS" AS comments,
    "COMPLEX_NAME" AS complex_name,
    "IRWINID" AS irwinid,
    "FIRE_NUM" AS fire_num,
    "COMPLEX_ID" AS complex_id,
    "DECADES" AS decades,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "california-department-of-finance-f3e56cb333394a9aba52f7f911197212"
