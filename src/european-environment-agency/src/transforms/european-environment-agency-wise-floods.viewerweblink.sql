SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("euUOMCode" AS VARCHAR) AS "euUOMCode",
    CAST("hyperlink" AS VARCHAR) AS "hyperlink",
    CAST("modelSchema" AS VARCHAR) AS "modelSchema"
FROM "european-environment-agency-wise-floods.viewerweblink"
