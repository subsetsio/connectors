-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Enterprise multifamily public-use rows are anonymized records with categorical loan and property attributes; record numbers are source identifiers within this public-use extract.
SELECT
    CAST("enterprise" AS BIGINT) AS enterprise,
    CAST("record_num_mf_nf" AS BIGINT) AS record_num_mf_nf,
    CAST("tract_minority_cat" AS BIGINT) AS tract_minority_cat,
    CAST("tract_income_cat" AS BIGINT) AS tract_income_cat,
    CAST("afford_mf" AS BIGINT) AS afford_mf,
    CAST("same_year_acq" AS BIGINT) AS same_year_acq,
    CAST("purpose_mf_nf" AS BIGINT) AS purpose_mf_nf,
    CAST("seller_type_mf_nf" AS BIGINT) AS seller_type_mf_nf,
    CAST("fed_guarantee_mf_nf" AS BIGINT) AS fed_guarantee_mf_nf,
    CAST("units_num_cat" AS BIGINT) AS units_num_cat
FROM "fhfa-pudb-enterprise-multifamily"
