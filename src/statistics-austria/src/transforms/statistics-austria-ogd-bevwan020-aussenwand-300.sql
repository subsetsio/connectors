-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "country_of_origin_destination",
    "nationality_pol_breakdown_level_3",
    "c_5_years_age_group",
    "in_migration_from_foreign_country",
    "out_migration_to_foreign_country"
FROM "statistics-austria-ogd-bevwan020-aussenwand-300"
