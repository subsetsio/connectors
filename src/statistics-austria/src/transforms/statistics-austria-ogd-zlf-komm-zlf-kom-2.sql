-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_period",
    "reporting_airport",
    "mode_of_traffic",
    "flights",
    "passengers_by_section_destination",
    "freight_in_kg",
    "mail_in_kg"
FROM "statistics-austria-ogd-zlf-komm-zlf-kom-2"
