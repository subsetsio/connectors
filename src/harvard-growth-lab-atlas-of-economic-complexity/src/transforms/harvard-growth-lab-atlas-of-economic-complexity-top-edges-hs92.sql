-- Residual edit over the compiled pass-through: the Product Space files ship
-- HS92 codes with leading zeros stripped ("101" for "0101"), so the compiler's
-- verified BIGINT cast would bake in a code that no longer joins the HS92
-- classification table. Left-pad to the 4-digit form instead.
-- caution: The Product Space network is undirected but every proximity link is stored twice, once in each direction — de-duplicate on the unordered pair before counting edges.
SELECT
    lpad(CAST("product_hs92_code_source" AS VARCHAR), 4, '0') AS product_hs92_code_source,
    lpad(CAST("product_hs92_code_target" AS VARCHAR), 4, '0') AS product_hs92_code_target
FROM "harvard-growth-lab-atlas-of-economic-complexity-top-edges-hs92"
