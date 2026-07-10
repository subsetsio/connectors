SELECT
    CAST("EEA_marine_assessment_area" AS VARCHAR) AS "EEA_marine_assessment_area",
    CAST("LastDiscodataUpdate" AS VARCHAR) AS "LastDiscodataUpdate",
    CAST("MPA_coverage_end2012_km2" AS VARCHAR) AS "MPA_coverage_end2012_km2",
    CAST("MPA_coverage_end2012_percent" AS VARCHAR) AS "MPA_coverage_end2012_percent",
    CAST("MPA_coverage_end2016_km2" AS VARCHAR) AS "MPA_coverage_end2016_km2",
    CAST("MPA_coverage_end2016_percent" AS VARCHAR) AS "MPA_coverage_end2016_percent",
    CAST("MPA_coverage_end2019_km2" AS VARCHAR) AS "MPA_coverage_end2019_km2",
    CAST("MPA_coverage_end2019_percent" AS VARCHAR) AS "MPA_coverage_end2019_percent",
    CAST("MPA_coverage_end2021_km2" AS VARCHAR) AS "MPA_coverage_end2021_km2",
    CAST("MPA_coverage_end2021_percent" AS VARCHAR) AS "MPA_coverage_end2021_percent",
    CAST("N2K_nearshore_end2021_percent" AS VARCHAR) AS "N2K_nearshore_end2021_percent",
    CAST("N2K_offshore_end2021_percent" AS VARCHAR) AS "N2K_offshore_end2021_percent",
    CAST("N2K_territorial_end2021_percent" AS VARCHAR) AS "N2K_territorial_end2021_percent"
FROM "european-environment-agency-wise-marine.marine-protected-areas"
