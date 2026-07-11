-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "key",
    "name",
    "description",
    "terms",
    "term_count"
FROM "inter-parliamentary-union-taxonomies"
