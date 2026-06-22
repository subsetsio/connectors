import os

# Per-report belief-test config, grounded in the live probe of each OASIS report.
# value_col: the report's MW/price column; date_col: the operating-date column;
# market_runs: the market_run_id values we query (enum only when we filter on it);
# opr_hr: whether the report carries the integer OPR_HR trading-hour column.
R = {
 "AS_OP_RSRV":      dict(value="MW",  date="OPR_DATE", mr=None,                     opr_hr=True),
 "AS_REQ":          dict(value="MW",  date="OPR_DT",   mr=["DAM","HASP"],           opr_hr=True),
 "AS_RESULTS":      dict(value="MW",  date="OPR_DT",   mr=["DAM","HASP"],           opr_hr=True),
 "CMMT_RA_MLC":     dict(value="MW",  date="OPR_DT",   mr=["DAM","RTM"],            opr_hr=True),
 "ENE_CB_AWARDS":   dict(value="MW",  date="OPR_DT",   mr=None,                     opr_hr=True),
 "ENE_CB_CLR_AWARDS":dict(value="MW", date="OPR_DT",   mr=None,                     opr_hr=True),
 "ENE_CB_MKT_SUM":  dict(value="TOTAL",date="OPR_DT",  mr=None,                     opr_hr=False),
 "ENE_DISP":        dict(value="MW",  date="OPR_DT",   mr=None,                     opr_hr=True),
 "ENE_EA":          dict(value="MW",  date="OPR_DT",   mr=None,                     opr_hr=True),
 "ENE_LOSS":        dict(value="VALUE",date="OPR_DT",  mr=["DAM","HASP"],           opr_hr=True),
 "ENE_SLRS":        dict(value="MW",  date="OPR_DT",   mr=["DAM","RUC","HASP","RTM"],opr_hr=True),
 "PRC_AS":          dict(value="MW",  date="OPR_DT",   mr=["DAM","HASP"],           opr_hr=True),
 "PRC_CNSTR":       dict(value="MW",  date="OPR_DT",   mr=["DAM","HASP","RTM"],     opr_hr=True),
 "PRC_FUEL":        dict(value="PRC", date="OPR_DT",   mr=None,                     opr_hr=True),
 "PRC_HASP_LMP":    dict(value="MW",  date="OPR_DT",   mr=["HASP"],                 opr_hr=True),
 "PRC_INTVL_AS":    dict(value="MW",  date="OPR_DT",   mr=["RTM"],                  opr_hr=True),
 "PRC_INTVL_LMP":   dict(value="MW",  date="OPR_DT",   mr=["RTM"],                  opr_hr=True),
 "PRC_LMP":         dict(value="MW",  date="OPR_DT",   mr=["DAM","RUC"],            opr_hr=True),
 "PRC_RTPD_LMP":    dict(value="MW",  date="OPR_DT",   mr=["RTPD"],                 opr_hr=True, inferred=True),
 "SLD_FCST":        dict(value="MW",  date="OPR_DT",   mr=["DAM","2DA","7DA","ACTUAL","RTM"], opr_hr=True),
 "SLD_FCST_PEAK":   dict(value="LOAD_MW",date="OPR_DT",mr=None,                     opr_hr=True),
 "SLD_REN_FCST":    dict(value="MW",  date="OPR_DT",   mr=["DAM","RTD","RTPD","ACTUAL"], opr_hr=True, inferred=True),
 "TRNS_ATC":        dict(value="MW",  date="OPR_DT",   mr=["DAM","HASP"],           opr_hr=True),
 "TRNS_OUTAGE":     dict(value="CURTAILED_OTC_MW",date="START_DATE",mr=None,        opr_hr=False),
 "TRNS_USAGE":      dict(value="MW",  date="OPR_DT",   mr=["DAM","HASP"],           opr_hr=True),
}

def yml_list(vals):
    return "[" + ", ".join(vals) + "]"

os.makedirs("tests", exist_ok=True)
for ent, c in R.items():
    sid = "caiso-" + ent.lower().replace("_", "-")
    inferred = c.get("inferred")
    lines = [f"spec_id: {sid}", "status: active", "tests:"]
    # Universal interval timestamps — present on every OASIS SingleZip CSV.
    lines += [
        "  - not_null: INTERVALSTARTTIME_GMT",
        "    reason: every OASIS report row is interval-stamped (GMT); a null means the CSV layout changed underneath us",
        "    certainty: 95",
        "  - not_null: INTERVALENDTIME_GMT",
        "    reason: paired with the start stamp on every row",
        "    certainty: 95",
        "  - column_type: {col: INTERVALSTARTTIME_GMT, type: string}",
        "    reason: OASIS emits ISO-8601 strings with a -0000 offset, parsed as text not native timestamps",
        "    certainty: 90",
    ]
    # Operating date.
    lines += [
        f"  - not_null: {c['date']}",
        f"    reason: the operating-date column is populated on every row of this report",
        "    certainty: 90",
    ]
    # Operating hour, where present.
    if c["opr_hr"]:
        lines += [
            "  - column_type: {col: OPR_HR, type: integer}",
            "    reason: OPR_HR is the integer CAISO trading hour",
            "    certainty: 85",
            "  - between: {col: OPR_HR, lo: 1, hi: 25}",
            "    reason: CAISO numbers hours 1..24 (25 on the fall back DST day)",
            "    certainty: 85",
            "    severity: warn",
        ]
    # Market-run enum, only where we filter by market_run_id.
    if c["mr"]:
        lines += [
            f"  - enum: {{col: MARKET_RUN_ID, values: {yml_list(c['mr'])}}}",
            "    reason: rows are filtered to the market_run_id values this report is queried for; an out-of-set value means the param contract changed",
            "    certainty: 85",
            "    severity: warn",
        ]
    # Value column populated for most rows.
    vc = c["value"]
    cert = 60 if inferred else 70
    lines += [
        f"  - nullable: {{col: {vc}, max_null_frac: 0.5}}",
        f"    reason: {vc} is the report's value column and is populated for the majority of rows",
        f"    certainty: {cert}",
        "    severity: warn",
    ]
    # Freshness — the backfill walks the window up to ~today.
    lines += [
        "  - freshness: {col: INTERVALSTARTTIME_GMT, reaches: today - 14d}",
        "    reason: the fetch walks the date window up to the current day, so the max interval should be recent",
        "    certainty: 60",
        "    points_outward: true",
        "    severity: warn",
    ]
    if inferred:
        lines.insert(2, "# NOTE: schema inferred by analogy (probe was throttled); reconcile on first materialization.")
    with open(f"tests/{sid}.yaml", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", sid)
print("total", len(R))
