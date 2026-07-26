-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bbl",
    "field",
    "old_value",
    "new_value",
    "_type" AS type,
    "reason",
    "_version" AS version
FROM "nyc-open-data-qt5r-nqxp"
