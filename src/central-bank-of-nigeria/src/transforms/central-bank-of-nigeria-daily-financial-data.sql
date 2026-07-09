-- one column per money-market operation; all amounts NGN million
SELECT
    CAST("id" AS BIGINT) AS source_row_id,
    CAST("recDate_iso" AS DATE) AS record_date,
    TRY_CAST(NULLIF(TRIM("opeBal"), '') AS DOUBLE) AS opening_balance,
    TRY_CAST(NULLIF(TRIM("rediscBills"), '') AS DOUBLE) AS rediscounted_bills,
    TRY_CAST(NULLIF(TRIM("slFacility"), '') AS DOUBLE) AS standing_lending_facility,
    TRY_CAST(NULLIF(TRIM("sdFacility"), '') AS DOUBLE) AS standing_deposit_facility,
    TRY_CAST(NULLIF(TRIM("repo"), '') AS DOUBLE) AS repo,
    TRY_CAST(NULLIF(TRIM("revRepo"), '') AS DOUBLE) AS reverse_repo,
    TRY_CAST(NULLIF(TRIM("omoSales"), '') AS DOUBLE) AS omo_sales,
    TRY_CAST(NULLIF(TRIM("omoRepay"), '') AS DOUBLE) AS omo_repayments,
    TRY_CAST(NULLIF(TRIM("pmSales"), '') AS DOUBLE) AS primary_market_sales,
    TRY_CAST(NULLIF(TRIM("pmRepay"), '') AS DOUBLE) AS primary_market_repayments,
    TRY_CAST(NULLIF(TRIM("crr"), '') AS DOUBLE) AS cash_reserve_requirement,
    TRY_CAST(NULLIF(TRIM("netWdas"), '') AS DOUBLE) AS net_wdas,
    TRY_CAST(NULLIF(TRIM("statAlloc"), '') AS DOUBLE) AS statutory_allocation,
    TRY_CAST(NULLIF(TRIM("jvCash"), '') AS DOUBLE) AS jv_cash_call,
    TRY_CAST(NULLIF(TRIM("netClr"), '') AS DOUBLE) AS net_clearing,
    TRY_CAST(NULLIF(TRIM("ndicPrem"), '') AS DOUBLE) AS ndic_premium,
    TRY_CAST(NULLIF(TRIM("oMajor"), '') AS DOUBLE) AS other_major
FROM "central-bank-of-nigeria-daily-financial-data"
