SELECT
    CAST("impact_description" AS VARCHAR) AS "impact_description",
    CAST("intensity" AS VARCHAR) AS "intensity",
    CAST("intensity_number" AS VARCHAR) AS "intensity_number",
    CAST("site_code" AS VARCHAR) AS "site_code"
FROM "european-environment-agency-bise.site-threats-pressures-impact-negative"
