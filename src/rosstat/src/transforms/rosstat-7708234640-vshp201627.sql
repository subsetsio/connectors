-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "MEASURES_" AS measures,
    "Oktmo_Parent" AS oktmo_parent,
    CAST("Category_Parent" AS BIGINT) AS category_parent,
    "Category_Gor_Sel" AS category_gor_sel,
    "Range32126_Code" AS range32126_code,
    "Range32126_Have" AS range32126_have,
    "Range31281_Code" AS range31281_code,
    "Range31281_Have" AS range31281_have,
    CAST("time" AS BIGINT) AS time,
    "value"
FROM "rosstat-7708234640-vshp201627"
