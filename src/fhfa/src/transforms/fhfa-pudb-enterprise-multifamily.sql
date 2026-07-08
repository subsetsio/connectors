SELECT
CAST(NULLIF(enterprise, '') AS BIGINT) AS enterprise,
CAST(NULLIF(record_num_mf_nf, '') AS BIGINT) AS record_num_mf_nf,
CAST(NULLIF(tract_minority_cat, '') AS BIGINT) AS tract_minority_cat,
CAST(NULLIF(tract_income_cat, '') AS BIGINT) AS tract_income_cat,
CAST(NULLIF(afford_mf, '') AS BIGINT) AS afford_mf,
CAST(NULLIF(same_year_acq, '') AS BIGINT) AS same_year_acq,
CAST(NULLIF(purpose_mf_nf, '') AS BIGINT) AS purpose_mf_nf,
CAST(NULLIF(seller_type_mf_nf, '') AS BIGINT) AS seller_type_mf_nf,
CAST(NULLIF(fed_guarantee_mf_nf, '') AS BIGINT) AS fed_guarantee_mf_nf,
CAST(NULLIF(units_num_cat, '') AS BIGINT) AS units_num_cat
FROM "fhfa-pudb-enterprise-multifamily"
