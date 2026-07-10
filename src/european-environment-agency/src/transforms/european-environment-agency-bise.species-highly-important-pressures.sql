SELECT
    CAST("code_pressure_threat" AS VARCHAR) AS "code_pressure_threat",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("label" AS VARCHAR) AS "label",
    CAST("quantity" AS VARCHAR) AS "quantity"
FROM "european-environment-agency-bise.species-highly-important-pressures"
