-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("canton_district_commune" AS VARCHAR) AS "canton_district_commune",
    CAST("citizenship_category_partner_1" AS VARCHAR) AS "citizenship_category_partner_1",
    CAST("citizenship_category_partner_2" AS VARCHAR) AS "citizenship_category_partner_2",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0102020202-102"
