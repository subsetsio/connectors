-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ccode1",
    "cowName1" AS cowname1,
    "ccode2",
    "cowName2" AS cowname2,
    "signDay" AS signday,
    "signMonth" AS signmonth,
    "signYear" AS signyear,
    "EIFDay" AS eifday,
    "EIFMonth" AS eifmonth,
    "EIFYear" AS eifyear,
    "type",
    "category1",
    "category2",
    "category3",
    "span",
    "renewType" AS renewtype,
    "renewYears" AS renewyears,
    "terminated",
    "durationActual" AS durationactual,
    "endYearEstimate" AS endyearestimate,
    "asymmetry",
    "categoryConf" AS categoryconf,
    "UNTS" AS unts,
    "fullText" AS fulltext,
    "sourceType" AS sourcetype,
    "source",
    "factivaConf" AS factivaconf,
    "factivaSign" AS factivasign,
    "factivaEIF" AS factivaeif,
    "DCAid" AS dcaid
FROM "correlates-of-war-dca-agreements"
