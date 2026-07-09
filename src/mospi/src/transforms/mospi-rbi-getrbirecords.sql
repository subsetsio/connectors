-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `year` mixes calendar years, fiscal-year labels and month-level periods; `month` is populated only for monthly series.
-- caution: `unit` varies by `indicator`; values are only comparable within one indicator.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "indicator",
    "year",
    "balance_of_payments",
    "trade_category",
    "value",
    "unit",
    "month",
    "category",
    "trade",
    "country_group",
    "country_sub_group",
    "countries",
    "currency",
    "reference_rate",
    "ex_rate_fluctuations",
    "commodities",
    "export_commodities",
    "external_debt_sector",
    "external_debt_other_sector",
    "external_debt_term",
    "external_debt_items",
    "foreign_exchange_reserve_type",
    "foreign_exchange_reserve_currency",
    "period",
    "import_commodities",
    "external_debt_agreement",
    "external_debt_category",
    "external_debt_sub_category",
    "external_debt_institutions",
    "bop_overall",
    "transaction_type",
    "quarter",
    "sub_category",
    "components",
    "sub_components",
    "currency_type",
    "NRI_deposits_sub_indicator" AS nri_deposits_sub_indicator,
    "NRI_deposits_category" AS nri_deposits_category,
    "transaction",
    "market",
    "conversion",
    "product",
    "trade_type"
FROM "mospi-rbi-getrbirecords"
