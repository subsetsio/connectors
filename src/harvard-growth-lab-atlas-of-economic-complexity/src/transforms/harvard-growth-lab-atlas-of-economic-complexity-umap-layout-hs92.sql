-- Residual edit over the compiled pass-through: the Product Space files ship
-- HS92 codes with leading zeros stripped ("101" for "0101"), so the compiler's
-- verified BIGINT cast would bake in a code that no longer joins the HS92
-- classification table. Left-pad to the 4-digit form instead.
-- caution: Covers only the 865 four-digit HS92 products drawn in the Product Space, not all 1,243 four-digit products in the HS92 codebook.
SELECT
    lpad(CAST("product_hs92_code" AS VARCHAR), 4, '0') AS product_hs92_code,
    "product_space_x",
    "product_space_y",
    "product_space_cluster_name"
FROM "harvard-growth-lab-atlas-of-economic-complexity-umap-layout-hs92"
