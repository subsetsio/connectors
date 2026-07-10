SELECT
    CAST("designated_area_type" AS VARCHAR) AS "designated_area_type",
    CAST("designation_type_code" AS VARCHAR) AS "designation_type_code",
    CAST("iucn_category" AS VARCHAR) AS "iucn_category",
    CAST("legal_foundation_year" AS VARCHAR) AS "legal_foundation_year",
    CAST("major_ecosystem_type" AS VARCHAR) AS "major_ecosystem_type",
    CAST("marine_area_percentage" AS VARCHAR) AS "marine_area_percentage",
    CAST("national_id" AS VARCHAR) AS "national_id",
    CAST("ps_local_id" AS VARCHAR) AS "ps_local_id",
    CAST("ps_namespace" AS VARCHAR) AS "ps_namespace",
    CAST("ps_version_id" AS VARCHAR) AS "ps_version_id",
    CAST("site_area" AS VARCHAR) AS "site_area",
    CAST("site_name" AS VARCHAR) AS "site_name"
FROM "european-environment-agency-eunis.natda-designated-site"
