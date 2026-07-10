-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("canton_district_commune" AS VARCHAR) AS "canton_district_commune",
    CAST("previous_citizenship_selection" AS VARCHAR) AS "previous_citizenship_selection",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0103030100-102"
