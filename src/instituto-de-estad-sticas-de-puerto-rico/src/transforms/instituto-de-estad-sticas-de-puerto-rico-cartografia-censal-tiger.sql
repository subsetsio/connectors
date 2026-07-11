-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("TLID" AS BIGINT) AS tlid,
    "FROMHN" AS fromhn,
    "TOHN" AS tohn,
    "SIDE" AS side,
    "ZIP" AS zip,
    "PLUS4" AS plus4,
    "FROMTYP" AS fromtyp,
    "TOTYP" AS totyp,
    CAST("ARID" AS BIGINT) AS arid,
    "MTFCC" AS mtfcc
FROM "instituto-de-estad-sticas-de-puerto-rico-cartografia-censal-tiger"
