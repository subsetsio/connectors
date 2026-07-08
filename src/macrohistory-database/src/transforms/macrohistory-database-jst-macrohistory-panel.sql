SELECT
    CAST(year AS INTEGER)   AS year,
    country,
    iso,
    CAST(ifs AS INTEGER)    AS ifs,
    pop, rgdpmad, rgdpbarro, rconsbarro, gdp, iy, cpi, ca,
    imports, exports, narrowm, money, stir, ltrate, hpnom,
    unemp, wage, debtgdp, revenue, expenditure, xrusd,
    tloans, tmort, thh, tbus, bdebt, lev, ltd, noncore,
    CAST(crisisJST AS INTEGER)     AS crisisJST,
    CAST(crisisJST_old AS INTEGER) AS crisisJST_old,
    CAST(peg AS INTEGER)           AS peg,
    CAST(peg_strict AS INTEGER)    AS peg_strict,
    peg_type, peg_base, JSTtrilemmaIV,
    eq_tr, housing_tr, bond_tr, bill_rate,
    CAST(rent_ipolated AS INTEGER)            AS rent_ipolated,
    CAST(housing_capgain_ipolated AS INTEGER) AS housing_capgain_ipolated,
    housing_capgain, housing_rent_rtn, housing_rent_yd,
    eq_capgain, eq_dp,
    CAST(eq_capgain_interp AS INTEGER) AS eq_capgain_interp,
    CAST(eq_tr_interp AS INTEGER)      AS eq_tr_interp,
    CAST(eq_dp_interp AS INTEGER)      AS eq_dp_interp,
    bond_rate, eq_div_rtn, capital_tr, risky_tr, safe_tr
FROM "macrohistory-database-jst-macrohistory-panel"
WHERE year IS NOT NULL AND country IS NOT NULL
ORDER BY country, year
