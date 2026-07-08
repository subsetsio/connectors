    SELECT

    CAST(report_date_as_yyyy_mm_dd[1:10] AS DATE)      AS report_date,
    market_and_exchange_names                          AS market,
    contract_market_name                               AS contract,
    cftc_contract_market_code                          AS cftc_code,
    cftc_market_code                                   AS exchange_code,
    commodity_name,
    commodity_group_name,
    commodity_subgroup_name,
    contract_units,
    TRY_CAST(open_interest_all AS DOUBLE)              AS open_interest,
    TRY_CAST(tot_rept_positions_long_all AS DOUBLE)    AS total_reportable_long,
    TRY_CAST(tot_rept_positions_short AS DOUBLE)       AS total_reportable_short,
    TRY_CAST(nonrept_positions_long_all AS DOUBLE)     AS nonreportable_long,
    TRY_CAST(nonrept_positions_short_all AS DOUBLE)    AS nonreportable_short,
    TRY_CAST(traders_tot_all AS DOUBLE)                AS total_traders
,
        futonly_or_combined                                AS report_type,
        TRY_CAST(change_in_open_interest_all AS DOUBLE)    AS change_in_open_interest,
        TRY_CAST(prod_merc_positions_long AS DOUBLE)       AS producer_merchant_long,
        TRY_CAST(prod_merc_positions_short AS DOUBLE)      AS producer_merchant_short,
        TRY_CAST(swap_positions_long_all AS DOUBLE)        AS swap_dealer_long,
        TRY_CAST(swap__positions_short_all AS DOUBLE)      AS swap_dealer_short,
        TRY_CAST(swap__positions_spread_all AS DOUBLE)     AS swap_dealer_spread,
        TRY_CAST(m_money_positions_long_all AS DOUBLE)     AS managed_money_long,
        TRY_CAST(m_money_positions_short_all AS DOUBLE)    AS managed_money_short,
        TRY_CAST(m_money_positions_spread AS DOUBLE)       AS managed_money_spread,
        TRY_CAST(other_rept_positions_long AS DOUBLE)      AS other_reportable_long,
        TRY_CAST(other_rept_positions_short AS DOUBLE)     AS other_reportable_short,
        TRY_CAST(other_rept_positions_spread AS DOUBLE)    AS other_reportable_spread
    FROM "cftc-disaggregated"
    WHERE report_date_as_yyyy_mm_dd IS NOT NULL
