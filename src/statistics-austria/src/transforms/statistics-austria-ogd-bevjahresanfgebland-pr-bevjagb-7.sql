-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "province_nuts_2_unit",
    CAST("year" AS BIGINT) AS year,
    "alter_in_15_jahresgruppen",
    "sex",
    "country_of_birth",
    "main_variant",
    "growth_scenario",
    "ageing_scenario",
    "upper_migration_variant",
    "lower_migration_variant",
    "upper_fertility_variant",
    "lower_fertility_variant",
    "upper_life_expectancy_variant",
    "lower_life_expectancy_variant",
    "status_quo_scenario",
    "zero_migration_scenario"
FROM "statistics-austria-ogd-bevjahresanfgebland-pr-bevjagb-7"
