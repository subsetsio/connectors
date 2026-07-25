-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "industries_nace_and_size_classes",
    "all_enterprises_with_technological_innovations",
    "enterprises_with_technological_innovations_in_house_r_d",
    "enterprises_with_technological_innovations_in_house_r_d_as_of_all_enterprises" AS entrprss_tchnlgcl_innvtns_in_hs_r_d_as_of_all_entrprss,
    "enterprises_with_technological_innovations_external_r_d",
    "enterprises_with_technological_innovations_external_r_d_as_of_all_enterprises" AS entrprss_tchnlgcl_innvtns_extrnl_r_d_as_of_all_entrprss,
    "expenditure_for_technological_innovations_2018_in_mio_eur_in_total" AS expndtr_fr_tchnlgcl_innvtns_2018_in_m_er_in_ttl,
    "expenditure_for_technological_innovations_2018_in_mio_eur_in_house_r_d" AS expndtr_fr_tchnlgcl_innvtns_2018_in_m_er_in_hs_r_d,
    "expenditure_for_technological_innovations_2018_in_mio_eur_external_r_d" AS expndtr_fr_tchnlgcl_innvtns_2018_in_m_er_extrnl_r_d,
    "expenditure_for_technological_innovations_2018_in_mio_eur_others"
FROM "statistics-austria-ogd-innov015-cis-015-unt-innovation-1"
