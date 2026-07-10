-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Enterprise single-family public-use rows are anonymized loan records; categorical fields should be treated as source codes unless FHFA documentation is consulted.
SELECT
    CAST("enterprise" AS BIGINT) AS enterprise,
    CAST("record_num_sf_nfb" AS BIGINT) AS record_num_sf_nfb,
    CAST("metro" AS BIGINT) AS metro,
    CAST("tract_minority_cat" AS BIGINT) AS tract_minority_cat,
    CAST("tract_income_cat" AS BIGINT) AS tract_income_cat,
    CAST("income_cat" AS BIGINT) AS income_cat,
    CAST("same_year_acq" AS BIGINT) AS same_year_acq,
    CAST("purpose_sf_nfb" AS BIGINT) AS purpose_sf_nfb,
    CAST("fed_guarantee_sf_nfb" AS BIGINT) AS fed_guarantee_sf_nfb,
    CAST("seller_type_sf_nfb" AS BIGINT) AS seller_type_sf_nfb,
    CAST("race_ethnicity_borr" AS BIGINT) AS race_ethnicity_borr,
    CAST("race_ethnicity_coborr" AS BIGINT) AS race_ethnicity_coborr,
    CAST("sex_borr" AS BIGINT) AS sex_borr,
    CAST("sex_coborr" AS BIGINT) AS sex_coborr,
    CAST("occupancy_sf_nfb" AS BIGINT) AS occupancy_sf_nfb,
    CAST("units_num" AS BIGINT) AS units_num,
    CAST("unit_own_occ" AS BIGINT) AS unit_own_occ,
    CAST("afford_sf" AS BIGINT) AS afford_sf
FROM "fhfa-pudb-enterprise-single-family"
