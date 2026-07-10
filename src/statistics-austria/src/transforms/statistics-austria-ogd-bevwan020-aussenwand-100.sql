-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "age_in_single_years",
    "nationality_aggregated_by_political_breakdown",
    "sex",
    "in_migration_from_foreign_country",
    "out_migration_to_foreign_country"
FROM "statistics-austria-ogd-bevwan020-aussenwand-100"
