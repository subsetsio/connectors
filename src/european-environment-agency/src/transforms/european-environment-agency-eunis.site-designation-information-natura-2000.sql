SELECT
    CAST("code_site" AS VARCHAR) AS "code_site",
    CAST("confirmed_date" AS VARCHAR) AS "confirmed_date",
    CAST("proposed_date" AS VARCHAR) AS "proposed_date",
    CAST("sac_date" AS VARCHAR) AS "sac_date",
    CAST("sci_check_mark" AS VARCHAR) AS "sci_check_mark",
    CAST("site_type" AS VARCHAR) AS "site_type",
    CAST("spa_check_mark" AS VARCHAR) AS "spa_check_mark",
    CAST("spa_date" AS VARCHAR) AS "spa_date",
    CAST("update_date" AS VARCHAR) AS "update_date"
FROM "european-environment-agency-eunis.site-designation-information-natura-2000"
