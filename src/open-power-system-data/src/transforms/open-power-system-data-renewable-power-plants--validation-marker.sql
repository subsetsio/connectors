-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a marker/code reference table for renewable plant validation status, not a plant inventory.
SELECT
    "Validation marker" AS validation_marker,
    "Long explanation" AS long_explanation,
    "Short explanation" AS short_explanation,
    "Country" AS country
FROM "open-power-system-data-renewable-power-plants--validation-marker"
