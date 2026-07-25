-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEASURES_" AS measures,
    CAST("Category_Parent" AS BIGINT) AS category_parent,
    "Oktmo_Parent" AS oktmo_parent,
    CAST("Dim01158_Code" AS BIGINT) AS dim01158_code,
    "Range01500_Code" AS range01500_code,
    "Range01500_Have" AS range01500_have,
    CAST("time" AS BIGINT) AS time,
    "value"
FROM "rosstat-7708234640-vshp2016511"
