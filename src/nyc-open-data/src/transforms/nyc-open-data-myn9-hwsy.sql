-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "exempt_code",
    "sdea_code",
    "description",
    "status",
    "legal_ref",
    "_comments" AS comments,
    "updated"
FROM "nyc-open-data-myn9-hwsy"
