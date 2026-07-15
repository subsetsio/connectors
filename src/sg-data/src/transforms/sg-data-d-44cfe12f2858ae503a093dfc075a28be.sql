-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "centre_code",
    "centre_name",
    "class_of_licence",
    "type_of_service",
    "levels_offered",
    "fees",
    "type_of_citizenship",
    "last_updated",
    "remarks"
FROM "sg-data-d-44cfe12f2858ae503a093dfc075a28be"
