-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The ASUT table combines SUPPLY, USE, and IOT matrices; `dom_imp` applies only to USE, so compare or aggregate within a single `tabletype` unless explicitly reconciling matrix concepts.
SELECT
    "cnt",
    "var",
    "year",
    "tabletype",
    "dom_imp",
    "row_industry",
    "col_industry",
    "value"
FROM "groningen-growth-and-development-centre-10.34894-imkxnt"
