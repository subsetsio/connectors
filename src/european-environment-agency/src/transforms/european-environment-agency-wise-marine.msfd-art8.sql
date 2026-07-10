SELECT
    CAST("AvgEUWatersRegionAreaNOOverlaps" AS VARCHAR) AS "AvgEUWatersRegionAreaNOOverlaps",
    CAST("Feature" AS VARCHAR) AS "Feature",
    CAST("GESAchievedBy2018" AS VARCHAR) AS "GESAchievedBy2018",
    CAST("GESNotAchievedBy2018" AS VARCHAR) AS "GESNotAchievedBy2018",
    CAST("LastDiscodataUpdate" AS VARCHAR) AS "LastDiscodataUpdate",
    CAST("MeasureNames" AS VARCHAR) AS "MeasureNames",
    CAST("NotAssessed" AS VARCHAR) AS "NotAssessed",
    CAST("NotReported" AS VARCHAR) AS "NotReported",
    CAST("Overlaps" AS VARCHAR) AS "Overlaps",
    CAST("Region" AS VARCHAR) AS "Region",
    CAST("SubRegion" AS VARCHAR) AS "SubRegion",
    CAST("TotalReportedArea" AS VARCHAR) AS "TotalReportedArea"
FROM "european-environment-agency-wise-marine.msfd-art8"
