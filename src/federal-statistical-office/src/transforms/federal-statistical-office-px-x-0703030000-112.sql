-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "forest_zone",
    "canton",
    "type_of_owner",
    "wood_species",
    "observation_unit",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0703030000-112"
