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
    "enterprises_with_technological_innovations_in_house_r_d_as_of_all_enterprises",
    "enterprises_with_technological_innovations_external_r_d",
    "enterprises_with_technological_innovations_external_r_d_as_of_all_enterprises",
    "expenditure_for_technological_innovations_2018_in_mio_eur_in_total",
    "expenditure_for_technological_innovations_2018_in_mio_eur_in_house_r_d",
    "expenditure_for_technological_innovations_2018_in_mio_eur_external_r_d",
    "expenditure_for_technological_innovations_2018_in_mio_eur_others"
FROM "statistics-austria-ogd-innov015-cis-015-unt-innovation-1"
