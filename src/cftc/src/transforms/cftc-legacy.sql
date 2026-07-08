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
        TRY_CAST(noncomm_positions_long_all AS DOUBLE)     AS noncommercial_long,
        TRY_CAST(noncomm_positions_short_all AS DOUBLE)    AS noncommercial_short,
        TRY_CAST(noncomm_postions_spread_all AS DOUBLE)    AS noncommercial_spread,
        TRY_CAST(comm_positions_long_all AS DOUBLE)        AS commercial_long,
        TRY_CAST(comm_positions_short_all AS DOUBLE)       AS commercial_short,
        TRY_CAST(conc_net_le_4_tdr_long_all AS DOUBLE)     AS conc_net_4_long_pct,
        TRY_CAST(conc_net_le_4_tdr_short_all AS DOUBLE)    AS conc_net_4_short_pct,
        TRY_CAST(conc_net_le_8_tdr_long_all AS DOUBLE)     AS conc_net_8_long_pct,
        TRY_CAST(conc_net_le_8_tdr_short_all AS DOUBLE)    AS conc_net_8_short_pct
    FROM "cftc-legacy"
    WHERE report_date_as_yyyy_mm_dd IS NOT NULL
