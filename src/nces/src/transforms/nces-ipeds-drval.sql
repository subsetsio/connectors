-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    CAST("LPBOOKSP" AS BIGINT) AS lpbooksp,
    CAST("LPMEDIAP" AS BIGINT) AS lpmediap,
    CAST("LPSERIAP" AS BIGINT) AS lpseriap,
    CAST("LEBOOKSP" AS BIGINT) AS lebooksp,
    CAST("LEDATABP" AS BIGINT) AS ledatabp,
    CAST("LEMEDIAP" AS BIGINT) AS lemediap,
    CAST("LESERIAP" AS BIGINT) AS leseriap,
    "LSALWAGP" AS lsalwagp,
    "LFRNGBNP" AS lfrngbnp,
    "LEXMSBBP" AS lexmsbbp,
    "LEXMSCSP" AS lexmscsp,
    "LEXMSOTP" AS lexmsotp,
    "LEXOMTLP" AS lexomtlp,
    "LEXPTOTF" AS lexptotf,
    "LTOTLFTE" AS ltotlfte,
    "LLIBRFTE" AS llibrfte,
    "LPROFFTE" AS lproffte,
    "LPAIDFTE" AS lpaidfte,
    "LSTUDFTE" AS lstudfte,
    "year"
FROM "nces-ipeds-drval"
