-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table mixes two observation frequencies. 33 early rows (1960-1992) are ANNUAL observations encoded with `tmonth` set equal to `tyear` and a `period` label of just the year (e.g. ` 1960`); the rest are true monthly observations with `tmonth` in 1..12. Filter on `tmonth <= 12` before treating the table as a monthly series, or annual and monthly levels will be interleaved.
-- caution: The aggregates are nested, not additive: `moneySupply_M3` contains `moneySupply_M2`, which in turn contains `narrowMoney` and `quasiMoney`. Summing the columns of a row is always wrong.
-- caution: All amounts are naira balances in millions, measured at end of period (a stock, not a flow) — differencing consecutive rows gives the flow.
-- caution: The M3-era columns (`moneySupply_M3`, `cbnBills`, `creditToGovernmentFed`, `mirrorAccounts`, `specialInterventionReserves`) only exist for the later part of the series; their absence in early rows is a definitional change, not a zero.
SELECT
    "id",
    "tyear",
    "tmonth",
    "period",
    "moneySupply_M3" AS moneysupply_m3,
    "cbnBills" AS cbnbills,
    CAST("moneySupply_M2" AS DOUBLE) AS moneysupply_m2,
    CAST("quasiMoney" AS DOUBLE) AS quasimoney,
    CAST("narrowMoney" AS DOUBLE) AS narrowmoney,
    CAST("currencyOutsideBanks" AS DOUBLE) AS currencyoutsidebanks,
    CAST("demandDeposits" AS DOUBLE) AS demanddeposits,
    CAST("netForeignAssets" AS DOUBLE) AS netforeignassets,
    CAST("netDomesticAssets" AS DOUBLE) AS netdomesticassets,
    CAST("netDomesticCredit" AS DOUBLE) AS netdomesticcredit,
    CAST("creditToGovernment" AS DOUBLE) AS credittogovernment,
    "creditToGovernmentFed" AS credittogovernmentfed,
    "mirrorAccounts" AS mirroraccounts,
    CAST("creditToPrivateSector" AS DOUBLE) AS credittoprivatesector,
    CAST("otherAssetsNet" AS DOUBLE) AS otherassetsnet,
    CAST("baseMoney" AS DOUBLE) AS basemoney,
    CAST("currencyInCirculation" AS DOUBLE) AS currencyincirculation,
    CAST("bankReserves" AS DOUBLE) AS bankreserves,
    "specialInterventionReserves" AS specialinterventionreserves
FROM "central-bank-of-nigeria-money-and-credit-statistics"
