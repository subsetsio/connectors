SELECT
    CAST("candidate_date" AS VARCHAR) AS "candidate_date",
    CAST("code_site" AS VARCHAR) AS "code_site",
    CAST("confirmed_date" AS VARCHAR) AS "confirmed_date",
    CAST("designation_date" AS VARCHAR) AS "designation_date",
    CAST("proposed_date" AS VARCHAR) AS "proposed_date",
    CAST("sci_check_mark" AS VARCHAR) AS "sci_check_mark",
    CAST("site_status" AS VARCHAR) AS "site_status",
    CAST("site_type" AS VARCHAR) AS "site_type",
    CAST("spa_check_mark" AS VARCHAR) AS "spa_check_mark",
    CAST("update_date" AS VARCHAR) AS "update_date"
FROM "european-environment-agency-eunis.site-designation-information-emerald"
