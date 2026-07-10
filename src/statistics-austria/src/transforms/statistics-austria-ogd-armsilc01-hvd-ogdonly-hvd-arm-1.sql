-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_serie" AS BIGINT) AS time_serie,
    "classifications",
    "people_at_risk_of_poverty_or_social_exclusion_rate",
    "at_risk_of_poverty_rate",
    "severe_material_and_social_deprivation_rate",
    "people_living_in_households_with_very_low_work_intensity_rate"
FROM "statistics-austria-ogd-armsilc01-hvd-ogdonly-hvd-arm-1"
