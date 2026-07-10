-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("duration_of_marriage" AS VARCHAR) AS "duration_of_marriage",
    CAST("age_class_partner_1" AS VARCHAR) AS "age_class_partner_1",
    CAST("age_class_partner_2" AS VARCHAR) AS "age_class_partner_2",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0102020203-104"
