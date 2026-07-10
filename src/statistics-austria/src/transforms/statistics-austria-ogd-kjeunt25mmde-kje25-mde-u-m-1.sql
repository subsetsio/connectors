-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "reference_month",
    "nace_2025_ebene_4",
    "number_of_enterprises_as_at_december_31",
    "persons_employed_total",
    "employees_total",
    "total_gross_earnings_in_thousand_eur",
    "total_turnover_in_thousand_eur",
    "domestic_turnover_in_thousand_eur"
FROM "statistics-austria-ogd-kjeunt25mmde-kje25-mde-u-m-1"
