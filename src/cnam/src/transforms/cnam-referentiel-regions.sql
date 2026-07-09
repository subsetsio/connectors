-- Published pass-through of raw asset `cnam-referentiel-regions`.
-- `reg_name_upper` (uppercase duplicate of the name) and `tri` (portal sort order) are dropped.
SELECT
    "reg_code" AS region_code,
    "reg_name" AS region_name,
    "reg_type" AS region_type
FROM "cnam-referentiel-regions"
