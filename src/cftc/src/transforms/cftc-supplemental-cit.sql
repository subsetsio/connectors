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
        'Combined'                                            AS report_type,
        TRY_CAST(change_open_interest_all AS DOUBLE)          AS change_in_open_interest,
        TRY_CAST(cit_positions_long_all AS DOUBLE)            AS index_trader_long,
        TRY_CAST(cit_positions_short_all AS DOUBLE)           AS index_trader_short,
        TRY_CAST("NComm_Postions_Long_All_NoCIT" AS DOUBLE)   AS noncommercial_long_excl_cit,
        TRY_CAST("NComm_Postions_Short_All_NoCIT" AS DOUBLE)  AS noncommercial_short_excl_cit,
        TRY_CAST("NComm_Postions_Spread_All_NoCIT" AS DOUBLE) AS noncommercial_spread_excl_cit,
        TRY_CAST(comm_positions_long_all_nocit AS DOUBLE)     AS commercial_long_excl_cit,
        TRY_CAST("Comm_Positions_Short_All_NoCIT" AS DOUBLE)  AS commercial_short_excl_cit
    FROM "cftc-supplemental-cit"
    WHERE report_date_as_yyyy_mm_dd IS NOT NULL
