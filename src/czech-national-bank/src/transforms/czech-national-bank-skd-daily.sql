SELECT DISTINCT
    CAST(settlementDate AS DATE)                AS settlement_date,
    isin,
    issueCode                                  AS issue_code,
    issueName                                  AS issue_name,
    CAST(nominalValueCZK AS DOUBLE)            AS nominal_value_czk,
    CAST(averagePriceToValue AS DOUBLE)        AS average_price_to_value,
    CAST(nominalValueOfSettlementCZK AS DOUBLE) AS nominal_value_of_settlement_czk
FROM "czech-national-bank-skd-daily"
WHERE settlementDate IS NOT NULL
  AND isin IS NOT NULL
  AND issueCode IS NOT NULL
