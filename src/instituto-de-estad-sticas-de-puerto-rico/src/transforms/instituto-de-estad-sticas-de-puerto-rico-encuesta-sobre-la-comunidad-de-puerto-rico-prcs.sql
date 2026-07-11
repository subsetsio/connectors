-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "PUMS Code" AS pums_code,
    "Ancestry Description" AS ancestry_description,
    "Ancestry Code" AS ancestry_code,
    "Corresponding Detailed Ancestry Code" AS corresponding_detailed_ancestry_code
FROM "instituto-de-estad-sticas-de-puerto-rico-encuesta-sobre-la-comunidad-de-puerto-rico-prcs"
