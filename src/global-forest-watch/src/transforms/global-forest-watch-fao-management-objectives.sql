-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Management-objective area measures are source categories that may overlap conceptually; do not treat every objective column as mutually exclusive land area without checking the FAO definition.
SELECT
    "iso",
    "country",
    "desk_study",
    "year",
    "production_ha",
    "protection_soil_water_ha",
    "conservation_biodiversity_ha",
    "social_services_ha",
    "multiple_use_ha",
    "other_ha",
    "none_or_unknown_ha"
FROM "global-forest-watch-fao-management-objectives"
