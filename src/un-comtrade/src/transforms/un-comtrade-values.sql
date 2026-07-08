SELECT
    CAST(refYear AS INTEGER)        AS year,
    CAST(reporterCode AS INTEGER)   AS reporter_code,
    any_value(reporterISO)          AS reporter_iso,
    any_value(reporterDesc)         AS reporter,
    CAST(partnerCode AS INTEGER)    AS partner_code,
    any_value(partnerISO)           AS partner_iso,
    any_value(partnerDesc)          AS partner,
    flowDesc                        AS flow,
    SUM(primaryValue)               AS trade_value_usd,
    bool_or(isReported)             AS is_reported
FROM "un-comtrade-values"
WHERE cmdCode = 'TOTAL'
  AND primaryValue IS NOT NULL
  AND refYear IS NOT NULL
  AND reporterCode IS NOT NULL
  AND partnerCode IS NOT NULL
  AND flowDesc IS NOT NULL
GROUP BY refYear, reporterCode, partnerCode, flowDesc
