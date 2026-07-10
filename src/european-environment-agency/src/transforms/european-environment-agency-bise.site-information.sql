SELECT
    CAST("area_ha" AS VARCHAR) AS "area_ha",
    CAST("area_km2" AS VARCHAR) AS "area_km2",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("designation" AS VARCHAR) AS "designation",
    CAST("major_ecosystem_type" AS VARCHAR) AS "major_ecosystem_type",
    CAST("management_plan" AS VARCHAR) AS "management_plan",
    CAST("natda_designation_national_language" AS VARCHAR) AS "natda_designation_national_language",
    CAST("number_protected_habitat_types" AS VARCHAR) AS "number_protected_habitat_types",
    CAST("number_protected_species" AS VARCHAR) AS "number_protected_species",
    CAST("regions" AS VARCHAR) AS "regions",
    CAST("site_code" AS VARCHAR) AS "site_code",
    CAST("site_description" AS VARCHAR) AS "site_description",
    CAST("site_name" AS VARCHAR) AS "site_name",
    CAST("site_type" AS VARCHAR) AS "site_type",
    CAST("year_stablished" AS VARCHAR) AS "year_stablished"
FROM "european-environment-agency-bise.site-information"
