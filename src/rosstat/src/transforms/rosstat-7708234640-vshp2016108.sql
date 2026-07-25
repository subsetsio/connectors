-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEASURES_" AS measures,
    "Oktmo_Parent" AS oktmo_parent,
    CAST("Category_Parent" AS BIGINT) AS category_parent,
    CAST("Dim01158_Code" AS BIGINT) AS dim01158_code,
    "Range01710_Have" AS range01710_have,
    CAST("Vkl_Type_Code" AS BIGINT) AS vkl_type_code,
    "Range01710_Code" AS range01710_code,
    CAST("time" AS BIGINT) AS time,
    "value"
FROM "rosstat-7708234640-vshp2016108"
