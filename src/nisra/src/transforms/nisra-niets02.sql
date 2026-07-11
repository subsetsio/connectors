-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "FLOW" AS flow,
    "Flow Label" AS flow_label,
    "TRANSACTION" AS transaction,
    "Transaction Label" AS transaction_label,
    "BROADDEST" AS broaddest,
    "Trade partner" AS trade_partner,
    "RUSECTION" AS rusection,
    "Industry sector" AS industry_sector,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-niets02"
