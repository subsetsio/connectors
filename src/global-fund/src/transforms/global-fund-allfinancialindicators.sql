-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are long-format financial observations across different indicator families and financial data sets; filter the relevant indicator and data set before aggregating values.
SELECT
    "financialIndicatorId" AS financialindicatorid,
    "indicatorName" AS indicatorname,
    "recordId" AS recordid,
    "activityAreaId" AS activityareaid,
    "financialCategoryId" AS financialcategoryid,
    "transactionDate" AS transactiondate,
    "startDate" AS startdate,
    "endDate" AS enddate,
    "periodCovered" AS periodcovered,
    CAST("periodFrom" AS BIGINT) AS periodfrom,
    CAST("periodTo" AS BIGINT) AS periodto,
    "isLatestReported" AS islatestreported,
    "isCumulative" AS iscumulative,
    "isAnnualized" AS isannualized,
    "providerRecordId" AS providerrecordid,
    "recieverRecordId" AS recieverrecordid,
    "valueDate" AS valuedate,
    "plannedAmountCurrency" AS plannedamountcurrency,
    "plannedAmount" AS plannedamount,
    "plannedAmountCumulative" AS plannedamountcumulative,
    "actualAmountCurrency" AS actualamountcurrency,
    "actualAmount" AS actualamount,
    "actualAmountCumulative" AS actualamountcumulative,
    "performance",
    "performanceCode" AS performancecode,
    "valueSource" AS valuesource,
    CAST("dateTimeCreated" AS TIMESTAMP) AS datetimecreated,
    "dateTimeUpdated" AS datetimeupdated,
    "financialDataSet" AS financialdataset
FROM "global-fund-allfinancialindicators"
