-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field and demographic characteristic" AS field_and_demographic_characteristic,
    "Total - Number" AS total_number,
    "One or more limitations of any type - Number" AS one_or_more_limitations_of_any_type_number,
    "One or more limitations of any type - Percent" AS one_or_more_limitations_of_any_type_percent,
    "Visual limitations - Number" AS visual_limitations_number,
    "Visual limitations - Percent" AS visual_limitations_percent,
    "Hearing limitations - Number" AS hearing_limitations_number,
    "Hearing limitations - Percent" AS hearing_limitations_percent,
    "Walking limitations - Number" AS walking_limitations_number,
    "Walking limitations - Percent" AS walking_limitations_percent,
    "Lifting limitations - Number" AS lifting_limitations_number,
    "Lifting limitations - Percent" AS lifting_limitations_percent,
    "Cognitive limitations - Number" AS cognitive_limitations_number,
    "Cognitive limitations - Percent" AS cognitive_limitations_percent
FROM "ncses-nsf25349-tab005-006"
