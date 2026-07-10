-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Month" AS BIGINT) AS month,
    "State" AS state,
    "Primary Mode" AS primary_mode,
    "Etiology" AS etiology,
    "Serotype or Genotype" AS serotype_or_genotype,
    "Etiology Status" AS etiology_status,
    "Setting" AS setting,
    CAST("Illnesses" AS BIGINT) AS illnesses,
    CAST("Hospitalizations" AS BIGINT) AS hospitalizations,
    CAST("Info On Hospitalizations" AS BIGINT) AS info_on_hospitalizations,
    CAST("Deaths" AS BIGINT) AS deaths,
    CAST("Info On Deaths" AS BIGINT) AS info_on_deaths,
    "Food Vehicle" AS food_vehicle,
    "Food Contaminated Ingredient" AS food_contaminated_ingredient,
    "IFSAC Category" AS ifsac_category,
    "Water Exposure" AS water_exposure,
    "Water Type" AS water_type,
    "Animal Type" AS animal_type
FROM "cdc-5xkq-dg7x"
