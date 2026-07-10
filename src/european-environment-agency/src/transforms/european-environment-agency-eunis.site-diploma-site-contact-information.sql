SELECT
    CAST("code_site" AS VARCHAR) AS "code_site",
    CAST("contact_international" AS VARCHAR) AS "contact_international",
    CAST("contact_local" AS VARCHAR) AS "contact_local",
    CAST("contact_national" AS VARCHAR) AS "contact_national",
    CAST("contact_regional" AS VARCHAR) AS "contact_regional",
    CAST("manager" AS VARCHAR) AS "manager",
    CAST("respondent" AS VARCHAR) AS "respondent"
FROM "european-environment-agency-eunis.site-diploma-site-contact-information"
