-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("jahr" AS BIGINT) AS jahr,
    "grossregion",
    "nettolohnhöhenklasse" AS nettolohnh_henklasse,
    "beschäftigungsgrad" AS besch_ftigungsgrad,
    "geschlecht",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0304010000-121"
