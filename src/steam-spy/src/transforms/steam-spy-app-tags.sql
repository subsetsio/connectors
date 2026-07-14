-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows contain tag vote counts from appdetails; applications without public tags are absent from this table.
SELECT
    "appid",
    "name",
    "tag",
    "votes"
FROM "steam-spy-app-tags"
