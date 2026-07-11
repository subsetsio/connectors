-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    CAST("FACSTAT" AS BIGINT) AS facstat,
    "XSISTOTL" AS xsistotl,
    CAST("SISTOTL" AS BIGINT) AS sistotl,
    "XSISPROF" AS xsisprof,
    CAST("SISPROF" AS BIGINT) AS sisprof,
    "XSISASCP" AS xsisascp,
    CAST("SISASCP" AS BIGINT) AS sisascp,
    "XSISASTP" AS xsisastp,
    CAST("SISASTP" AS BIGINT) AS sisastp,
    "XSISINST" AS xsisinst,
    CAST("SISINST" AS BIGINT) AS sisinst,
    "XSISLECT" AS xsislect,
    CAST("SISLECT" AS BIGINT) AS sislect,
    "XSISNORK" AS xsisnork,
    CAST("SISNORK" AS BIGINT) AS sisnork,
    "year"
FROM "nces-ipeds-s-sis"
