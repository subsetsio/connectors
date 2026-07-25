-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "industries_nace_and_size_classes",
    "turnover_with_product_innovations_in_million_euro",
    "turnover_with_product_innovations_as_of_total_turnover",
    "turnover_with_product_innovations_in_million_euro_of_which_market_novelties" AS trnvr_prdct_innvtns_in_mlln_er_of_whch_mrkt_nvlts,
    "turnover_with_product_innovations_in_million_euro_of_which_market_novelties_as_of_total_turnover" AS trnvr_prdct_innvtns_in_mlln_er_of_whch_mrkt_nvlts_as_of_ttl_trnv,
    "turnover_with_product_innovations_in_million_euro_of_which_products_only_new_to_the_firm" AS trnvr_prdct_innvtns_in_mlln_er_of_whch_prdcts_only_nw_t_th_frm,
    "turnover_with_product_innovations_only_new_to_the_firm_as_of_total_turnover" AS trnvr_prdct_innvtns_only_nw_t_th_frm_as_of_ttl_trnvr
FROM "statistics-austria-ogd-innov014-cis-014-unt-innovation-1"
