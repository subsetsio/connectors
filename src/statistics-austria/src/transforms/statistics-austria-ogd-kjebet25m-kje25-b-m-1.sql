-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "nace_2025_teilw_abo_ebene_4",
    "berichtsmonat",
    "establishments",
    "persons_employed_total",
    "employees_total",
    "total_gross_earnings_in_thousand_eur",
    "total_hours_worked",
    "production_sold_in_thousand_eur",
    "total_technical_production_in_thousand_eur"
FROM "statistics-austria-ogd-kjebet25m-kje25-b-m-1"
