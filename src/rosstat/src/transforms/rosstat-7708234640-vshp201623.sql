-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEASURES_" AS measures,
    "Oktmo_Parent" AS oktmo_parent,
    "Category_Parent" AS category_parent,
    "Range01168_Code" AS range01168_code,
    CAST("Dim01158_Code" AS BIGINT) AS dim01158_code,
    CAST("Vkl_Type_Code" AS BIGINT) AS vkl_type_code,
    CAST("time" AS BIGINT) AS time,
    "value"
FROM "rosstat-7708234640-vshp201623"
