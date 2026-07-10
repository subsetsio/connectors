-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "province",
    "component",
    "main_scenario",
    "growth_scenario",
    "ageing_scenario",
    "upper_migration_scenario",
    "lower_migration_scenario",
    "upper_fertility_scenario",
    "lower_fertility_scenario",
    "upper_life_expectancy_scenario",
    "lower_life_expectancy_scenario",
    "status_quo_scenario",
    "zero_migration_scenario"
FROM "statistics-austria-ogd-bevbewegung-bev-bew-3"
