-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEASURES_" AS measures,
    "Oktmo_Parent" AS oktmo_parent,
    CAST("Category_Parent" AS BIGINT) AS category_parent,
    CAST("Dim01158_Code" AS BIGINT) AS dim01158_code,
    CAST("Vkl_Type_Code" AS BIGINT) AS vkl_type_code,
    "Range325_Code" AS range325_code,
    "Range325_Have" AS range325_have,
    CAST("time" AS BIGINT) AS time,
    "value"
FROM "rosstat-7708234640-vshp201694"
