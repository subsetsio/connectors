SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("FigureNumber" AS VARCHAR) AS "FigureNumber",
    CAST("TimePeriod" AS VARCHAR) AS "TimePeriod",
    CAST("Unit" AS VARCHAR) AS "Unit",
    CAST("Value" AS VARCHAR) AS "Value",
    CAST("Variable" AS VARCHAR) AS "Variable"
FROM "european-environment-agency-digitalwater.cp-allfigures"
