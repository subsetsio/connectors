-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEASURES_" AS measures,
    "Oktmo_Parent" AS oktmo_parent,
    CAST("Category_Parent" AS BIGINT) AS category_parent,
    "Dim_Okopf_F" AS dim_okopf_f,
    "Dim01158_Code" AS dim01158_code,
    "Range01168_Have" AS range01168_have,
    "Range01500_Have" AS range01500_have,
    "Range01710_Have" AS range01710_have,
    "Range322_Have" AS range322_have,
    "Range01755_Have" AS range01755_have,
    "Range01806_Have" AS range01806_have,
    CAST("time" AS BIGINT) AS time,
    "value"
FROM "rosstat-7708234640-vshp20164"
