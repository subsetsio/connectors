-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "settlementDate" AS settlementdate,
    "isin",
    "issueCode" AS issuecode,
    "issueName" AS issuename,
    CAST("nominalValueCZK" AS BIGINT) AS nominalvalueczk,
    "averagePriceToValue" AS averagepricetovalue,
    "nominalValueOfSettlementCZK" AS nominalvalueofsettlementczk
FROM "czech-national-bank-skd-daily"
