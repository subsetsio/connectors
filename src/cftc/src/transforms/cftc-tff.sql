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
        TRY_CAST(dealer_positions_long_all AS DOUBLE)      AS dealer_long,
        TRY_CAST(dealer_positions_short_all AS DOUBLE)     AS dealer_short,
        TRY_CAST(dealer_positions_spread_all AS DOUBLE)    AS dealer_spread,
        TRY_CAST(asset_mgr_positions_long AS DOUBLE)       AS asset_manager_long,
        TRY_CAST(asset_mgr_positions_short AS DOUBLE)      AS asset_manager_short,
        TRY_CAST(asset_mgr_positions_spread AS DOUBLE)     AS asset_manager_spread,
        TRY_CAST(lev_money_positions_long AS DOUBLE)       AS leveraged_funds_long,
        TRY_CAST(lev_money_positions_short AS DOUBLE)      AS leveraged_funds_short,
        TRY_CAST(lev_money_positions_spread AS DOUBLE)     AS leveraged_funds_spread,
        TRY_CAST(other_rept_positions_long AS DOUBLE)      AS other_reportable_long,
        TRY_CAST(other_rept_positions_short AS DOUBLE)     AS other_reportable_short,
        TRY_CAST(other_rept_positions_spread AS DOUBLE)    AS other_reportable_spread
    FROM "cftc-tff"
    WHERE report_date_as_yyyy_mm_dd IS NOT NULL
