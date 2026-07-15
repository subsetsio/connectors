-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "accident_classification",
    "road_user_group",
    "causes_of_accident",
    "number_of_accidents"
FROM "sg-data-d-d085ce60a604f938aff6779ed08a106a"
