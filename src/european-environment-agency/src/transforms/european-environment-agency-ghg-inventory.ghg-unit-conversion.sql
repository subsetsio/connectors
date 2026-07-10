SELECT
    CAST("multiplier" AS VARCHAR) AS "multiplier",
    CAST("unit_id_from" AS VARCHAR) AS "unit_id_from",
    CAST("unit_id_to" AS VARCHAR) AS "unit_id_to"
FROM "european-environment-agency-ghg-inventory.ghg-unit-conversion"
