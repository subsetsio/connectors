SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("CountryName" AS VARCHAR) AS "CountryName",
    CAST("Discodata_update_marine" AS VARCHAR) AS "Discodata_update_marine",
    CAST("Discodata_update_terrestrial" AS VARCHAR) AS "Discodata_update_terrestrial",
    CAST("LandBothArea" AS VARCHAR) AS "LandBothArea",
    CAST("LandN2KAreaonly" AS VARCHAR) AS "LandN2KAreaonly",
    CAST("LandNDAAreaOnly" AS VARCHAR) AS "LandNDAAreaOnly",
    CAST("marineBothArea" AS VARCHAR) AS "marineBothArea",
    CAST("MarineN2KAreaOnly" AS VARCHAR) AS "MarineN2KAreaOnly",
    CAST("MarineNDAreaOnly" AS VARCHAR) AS "MarineNDAreaOnly",
    CAST("NumberN2K" AS VARCHAR) AS "NumberN2K",
    CAST("NumberSCI" AS VARCHAR) AS "NumberSCI",
    CAST("NumberSPA" AS VARCHAR) AS "NumberSPA",
    CAST("Temporal_coverage" AS VARCHAR) AS "Temporal_coverage"
FROM "european-environment-agency-bise.protectedareas-stats-specific-cp-2022"
