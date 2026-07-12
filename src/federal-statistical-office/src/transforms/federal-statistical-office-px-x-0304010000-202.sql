-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("jahr" AS BIGINT) AS jahr,
    "grossregion",
    "ausbildung",
    "berufliche_stellung",
    "geschlecht",
    "zentralwert_und_andere_perzentile",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0304010000-202"
