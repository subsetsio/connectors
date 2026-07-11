-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    "SALTOTL" AS saltotl,
    "SALPROF" AS salprof,
    "SALASSC" AS salassc,
    "SALASST" AS salasst,
    "SALINST" AS salinst,
    "SALLECT" AS sallect,
    "SALNRNK" AS salnrnk,
    CAST("SFTETOTL" AS BIGINT) AS sftetotl,
    CAST("SFTEPSTC" AS BIGINT) AS sftepstc,
    CAST("SFTEINST" AS BIGINT) AS sfteinst,
    CAST("SFTERSRC" AS BIGINT) AS sftersrc,
    CAST("SFTEPBSV" AS BIGINT) AS sftepbsv,
    CAST("SFTELCAI" AS BIGINT) AS sftelcai,
    CAST("SFTELCA" AS BIGINT) AS sftelca,
    CAST("SFTEOTIS" AS BIGINT) AS sfteotis,
    CAST("SFTEMNGM" AS BIGINT) AS sftemngm,
    CAST("SFTEBFO" AS BIGINT) AS sftebfo,
    CAST("SFTECES" AS BIGINT) AS sfteces,
    CAST("SFTECLAM" AS BIGINT) AS sfteclam,
    CAST("SFTEHLTH" AS BIGINT) AS sftehlth,
    CAST("SFTEOTHR" AS BIGINT) AS sfteothr,
    CAST("SFTESRVC" AS BIGINT) AS sftesrvc,
    CAST("SFTESALE" AS BIGINT) AS sftesale,
    CAST("SFTEOFAS" AS BIGINT) AS sfteofas,
    CAST("SFTENRCM" AS BIGINT) AS sftenrcm,
    CAST("SFTEPTMM" AS BIGINT) AS sfteptmm,
    "year"
FROM "nces-ipeds-drvhr"
