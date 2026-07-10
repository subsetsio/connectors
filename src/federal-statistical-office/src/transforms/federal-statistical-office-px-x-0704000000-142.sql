-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kontoposten" AS VARCHAR) AS "kontoposten",
    CAST("bereich_der_forstwirtschaft" AS VARCHAR) AS "bereich_der_forstwirtschaft",
    CAST("typ_des_holzvorrates" AS VARCHAR) AS "typ_des_holzvorrates",
    CAST("einheit" AS VARCHAR) AS "einheit",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0704000000-142"
