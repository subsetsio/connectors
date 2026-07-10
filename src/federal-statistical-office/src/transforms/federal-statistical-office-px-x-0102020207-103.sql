-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("sex_of_child" AS VARCHAR) AS "sex_of_child",
    CAST("age_class_of_child" AS VARCHAR) AS "age_class_of_child",
    CAST("citizenship_category_of_father" AS VARCHAR) AS "citizenship_category_of_father",
    CAST("citizenship_category_of_mother" AS VARCHAR) AS "citizenship_category_of_mother",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0102020207-103"
