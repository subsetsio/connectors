-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "- 1 -" AS "1"
FROM "instituto-de-estad-sticas-de-puerto-rico-mortalidad-por-causas-multiples"
