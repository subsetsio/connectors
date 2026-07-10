SELECT
    CAST("code_designation" AS VARCHAR) AS "code_designation",
    CAST("code_site" AS VARCHAR) AS "code_site",
    CAST("designation_year" AS VARCHAR) AS "designation_year",
    CAST("english_name" AS VARCHAR) AS "english_name",
    CAST("national_category" AS VARCHAR) AS "national_category",
    CAST("national_category_description" AS VARCHAR) AS "national_category_description",
    CAST("original_name" AS VARCHAR) AS "original_name"
FROM "european-environment-agency-eunis.site-designation-information-natda"
