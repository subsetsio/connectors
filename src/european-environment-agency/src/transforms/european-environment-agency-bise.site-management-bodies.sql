SELECT
    CAST("org_address_unstructured" AS VARCHAR) AS "org_address_unstructured",
    CAST("org_email" AS VARCHAR) AS "org_email",
    CAST("org_name" AS VARCHAR) AS "org_name",
    CAST("site_code" AS VARCHAR) AS "site_code"
FROM "european-environment-agency-bise.site-management-bodies"
