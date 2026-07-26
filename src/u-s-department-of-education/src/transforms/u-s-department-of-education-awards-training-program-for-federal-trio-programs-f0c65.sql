-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "row_number",
    "��ࡱ�" AS column,
    "" AS column_2,
    "A" AS a,
    "C" AS c,
    "C.1" AS c_1,
    "C.2" AS c_2,
    "C.3" AS c_3,
    "C.4" AS c_4,
    "A.1" AS a_1,
    "C.5" AS c_5,
    "A.2" AS a_2,
    "A.3" AS a_3,
    "C.6" AS c_6
FROM "u-s-department-of-education-awards-training-program-for-federal-trio-programs-f0c65"
