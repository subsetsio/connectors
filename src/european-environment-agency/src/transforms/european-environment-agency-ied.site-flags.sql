SELECT
    CAST("count_factype_EPRTR" AS VARCHAR) AS "count_factype_EPRTR",
    CAST("count_factype_NONEPRTR" AS VARCHAR) AS "count_factype_NONEPRTR",
    CAST("count_instype_IED" AS VARCHAR) AS "count_instype_IED",
    CAST("count_instype_NONIED" AS VARCHAR) AS "count_instype_NONIED",
    CAST("count_plantType_coWI" AS VARCHAR) AS "count_plantType_coWI",
    CAST("count_plantType_LCP" AS VARCHAR) AS "count_plantType_LCP",
    CAST("count_plantType_WI" AS VARCHAR) AS "count_plantType_WI",
    CAST("has_facilities" AS VARCHAR) AS "has_facilities",
    CAST("has_fuel_data" AS VARCHAR) AS "has_fuel_data",
    CAST("has_installations" AS VARCHAR) AS "has_installations",
    CAST("has_lcps" AS VARCHAR) AS "has_lcps",
    CAST("has_ophours_data" AS VARCHAR) AS "has_ophours_data",
    CAST("has_release_data" AS VARCHAR) AS "has_release_data",
    CAST("has_seveso" AS VARCHAR) AS "has_seveso",
    CAST("has_transfer_data" AS VARCHAR) AS "has_transfer_data",
    CAST("has_waste_data" AS VARCHAR) AS "has_waste_data",
    CAST("Site Inspire ID" AS VARCHAR) AS "Site Inspire ID"
FROM "european-environment-agency-ied.site-flags"
