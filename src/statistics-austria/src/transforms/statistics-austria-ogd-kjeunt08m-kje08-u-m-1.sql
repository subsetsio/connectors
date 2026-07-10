-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "reference_month",
    "nace_2008_teilw_abo_ebene_4",
    "enterprises",
    "persons_employed_total",
    "total_gross_earnings_in_thousand_eur",
    "total_turnover_in_thousand_eur",
    "domestic_turnover_in_thousand_eur",
    "turnover_in_thousand_eur_eurozone_countries_without_austria",
    "turnover_from_in_thousand_eur_non_eurozone_countries_and_third_countries"
FROM "statistics-austria-ogd-kjeunt08m-kje08-u-m-1"
