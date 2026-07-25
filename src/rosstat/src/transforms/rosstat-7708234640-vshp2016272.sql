-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEASURES_" AS measures,
    CAST("Category_Parent" AS BIGINT) AS category_parent,
    "Oktmo_Parent" AS oktmo_parent,
    CAST("Vkl_Type_Code" AS BIGINT) AS vkl_type_code,
    "Range01204_Code" AS range01204_code,
    "Range01204_Have" AS range01204_have,
    CAST("time" AS BIGINT) AS time,
    "value"
FROM "rosstat-7708234640-vshp2016272"
