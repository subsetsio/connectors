SELECT
    CAST("classification" AS VARCHAR) AS "classification",
    CAST("cs_country_code" AS VARCHAR) AS "cs_country_code",
    CAST("gas" AS VARCHAR) AS "gas",
    CAST("gwp_coefficient" AS VARCHAR) AS "gwp_coefficient",
    CAST("heading" AS VARCHAR) AS "heading",
    CAST("is_country_specific" AS VARCHAR) AS "is_country_specific",
    CAST("is_template" AS VARCHAR) AS "is_template",
    CAST("measure" AS VARCHAR) AS "measure",
    CAST("navigation" AS VARCHAR) AS "navigation",
    CAST("parameter" AS VARCHAR) AS "parameter",
    CAST("sector" AS VARCHAR) AS "sector",
    CAST("sector_number" AS VARCHAR) AS "sector_number",
    CAST("template_var_uid" AS VARCHAR) AS "template_var_uid",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("unit_id" AS VARCHAR) AS "unit_id",
    CAST("variable_name" AS VARCHAR) AS "variable_name",
    CAST("variable_uid" AS VARCHAR) AS "variable_uid"
FROM "european-environment-agency-ghg-inventory.ghg-variable"
