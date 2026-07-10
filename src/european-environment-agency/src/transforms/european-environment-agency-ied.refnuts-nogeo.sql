SELECT
    CAST("CNTR_CODE" AS VARCHAR) AS "CNTR_CODE",
    CAST("id" AS VARCHAR) AS "id",
    CAST("LEVL_CODE" AS VARCHAR) AS "LEVL_CODE",
    CAST("NUTS_ID" AS VARCHAR) AS "NUTS_ID",
    CAST("NUTS_NAME" AS VARCHAR) AS "NUTS_NAME",
    CAST("shape_wm_as_text" AS VARCHAR) AS "shape_wm_as_text",
    CAST("shape_wm_srid" AS VARCHAR) AS "shape_wm_srid"
FROM "european-environment-agency-ied.refnuts-nogeo"
