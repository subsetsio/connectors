-- Published pass-through of raw asset `cnam-referentiel-departements`.
-- `dep_name_upper` (uppercase duplicate of the name) and `tri` (portal sort order) are dropped.
SELECT
    "dep_code" AS department_code,
    "dep_name" AS department_name,
    "dep_type" AS department_type,
    "reg_code" AS region_code,
    "reg_name" AS region_name
FROM "cnam-referentiel-departements"
