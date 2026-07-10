-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "OAS_Number" AS oas_number,
    "Verified" AS verified,
    "Country" AS country,
    "State" AS state,
    "City" AS city,
    "Lat_DMS" AS lat_dms,
    "Long_DMS" AS long_dms,
    CAST("Lat_DD" AS DOUBLE) AS lat_dd,
    CAST("Long_DD" AS DOUBLE) AS long_dd,
    "Type_Code" AS type_code,
    CAST("Quantity" AS BIGINT) AS quantity,
    "AGL" AS agl,
    "AMSL" AS amsl,
    "Lighting" AS lighting,
    "Horizontal" AS horizontal,
    "Vertical" AS vertical,
    "Marking" AS marking,
    "Study" AS study,
    "Action" AS action,
    CAST("Date" AS BIGINT) AS date
FROM "faa-digital-obstacle-file"
