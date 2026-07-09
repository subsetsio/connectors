-- `frequency` is derived from the source's tmonth-holds-the-year encoding for the 33 pre-1993 annual rows
-- `month` is nulled on those rows rather than left holding a year
SELECT
    CAST("id" AS BIGINT) AS source_row_id,
    CAST("period_start_iso" AS DATE) AS period_start,
    CASE WHEN "tmonth" BETWEEN 1 AND 12 THEN 'monthly' ELSE 'annual' END AS frequency,
    CAST("tyear" AS BIGINT) AS year,
    CASE WHEN "tmonth" BETWEEN 1 AND 12 THEN CAST("tmonth" AS BIGINT) END AS month,
    TRY_CAST(NULLIF(TRIM("moneySupply_M3"), '') AS DOUBLE) AS money_supply_m3,
    TRY_CAST(NULLIF(TRIM("cbnBills"), '') AS DOUBLE) AS cbn_bills,
    TRY_CAST(NULLIF(TRIM("moneySupply_M2"), '') AS DOUBLE) AS money_supply_m2,
    TRY_CAST(NULLIF(TRIM("quasiMoney"), '') AS DOUBLE) AS quasi_money,
    TRY_CAST(NULLIF(TRIM("narrowMoney"), '') AS DOUBLE) AS narrow_money,
    TRY_CAST(NULLIF(TRIM("currencyOutsideBanks"), '') AS DOUBLE) AS currency_outside_banks,
    TRY_CAST(NULLIF(TRIM("demandDeposits"), '') AS DOUBLE) AS demand_deposits,
    TRY_CAST(NULLIF(TRIM("netForeignAssets"), '') AS DOUBLE) AS net_foreign_assets,
    TRY_CAST(NULLIF(TRIM("netDomesticAssets"), '') AS DOUBLE) AS net_domestic_assets,
    TRY_CAST(NULLIF(TRIM("netDomesticCredit"), '') AS DOUBLE) AS net_domestic_credit,
    TRY_CAST(NULLIF(TRIM("creditToGovernment"), '') AS DOUBLE) AS credit_to_government,
    TRY_CAST(NULLIF(TRIM("creditToGovernmentFed"), '') AS DOUBLE) AS credit_to_government_federal,
    TRY_CAST(NULLIF(TRIM("mirrorAccounts"), '') AS DOUBLE) AS mirror_accounts,
    TRY_CAST(NULLIF(TRIM("creditToPrivateSector"), '') AS DOUBLE) AS credit_to_private_sector,
    TRY_CAST(NULLIF(TRIM("otherAssetsNet"), '') AS DOUBLE) AS other_assets_net,
    TRY_CAST(NULLIF(TRIM("baseMoney"), '') AS DOUBLE) AS base_money,
    TRY_CAST(NULLIF(TRIM("currencyInCirculation"), '') AS DOUBLE) AS currency_in_circulation,
    TRY_CAST(NULLIF(TRIM("bankReserves"), '') AS DOUBLE) AS bank_reserves,
    TRY_CAST(NULLIF(TRIM("specialInterventionReserves"), '') AS DOUBLE) AS special_intervention_reserves
FROM "central-bank-of-nigeria-money-and-credit-statistics"
