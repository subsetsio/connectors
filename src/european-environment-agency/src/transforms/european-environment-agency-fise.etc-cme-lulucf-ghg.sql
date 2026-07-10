SELECT
    CAST("Cropland" AS VARCHAR) AS "Cropland",
    CAST("Forest_Land" AS VARCHAR) AS "Forest_Land",
    CAST("Grassland" AS VARCHAR) AS "Grassland",
    CAST("HWPs" AS VARCHAR) AS "HWPs",
    CAST("LULUCF_WAM" AS VARCHAR) AS "LULUCF_WAM",
    CAST("LULUCF_WEM" AS VARCHAR) AS "LULUCF_WEM",
    CAST("Other" AS VARCHAR) AS "Other",
    CAST("Other_land" AS VARCHAR) AS "Other_land",
    CAST("Settlements" AS VARCHAR) AS "Settlements",
    CAST("Submission_date" AS VARCHAR) AS "Submission_date",
    CAST("Total_LULUCF" AS VARCHAR) AS "Total_LULUCF",
    CAST("Unit" AS VARCHAR) AS "Unit",
    CAST("Wetlands" AS VARCHAR) AS "Wetlands",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.etc-cme-lulucf-ghg"
