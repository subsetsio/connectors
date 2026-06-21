import json, os

ROOT = "/Users/nathansnellaert/Documents/hardened"
coll = json.load(open(f"{ROOT}/data/sources/economic-policy-institute/assets/collect/indicators/current.json"))
union = json.load(open(f"{ROOT}/data/sources/economic-policy-institute/work/entity_union.json"))
union_ids = union if isinstance(union, list) else list(union.keys() if isinstance(union, dict) else union)
# union may be {"entities":[...]} or list; normalize
if isinstance(union, dict):
    # find the list
    for v in union.values():
        if isinstance(v, list):
            union_ids = v; break
print("union ids:", len(union_ids))

# name -> filename observed from the ZIP (probe3)
name_to_file = {
 "Median household income":"median_household_income.csv",
 "Annual wages for select wage groups":"annual_wages_for_select_wage_groups.csv",
 "CEO pay ratio":"ceo_pay_ratio.csv",
 "Black-white wage gap":"black_white_wage_gap.csv",
 "Gender wage gap":"gender_wage_gap.csv",
 "Hispanic-white wage gap":"hispanic_white_wage_gap.csv",
 "Hourly wage, average":"hourly_wage_average.csv",
 "Hourly wage, median":"hourly_wage_median.csv",
 "Hourly earnings by industry":"hourly_earnings_by_industry.csv",
 "Hourly wage percentile ratios":"hourly_wage_percentile_ratios.csv",
 "Hourly wage percentiles":"hourly_wage_percentiles.csv",
 "College wage premium":"college_wage_premium.csv",
 "Time at work":"time_at_work.csv",
 "Employment by demographics":"employment_by_demographics.csv",
 "Labor force participation":"labor_force_participation.csv",
 "Long-term unemployment":"long_term_unemployment.csv",
 "Multiple jobs":"multiple_jobs.csv",
 "Employment by industry (CES)":"employment_by_industry_ces.csv",
 "Part-time employment":"part_time_employment.csv",
 "Part-time for economic reasons":"part_time_for_economic_reasons.csv",
 "Underemployment":"underemployment.csv",
 "Unemployment":"unemployment.csv",
 "Minimum wage":"minimum_wage.csv",
 "Civilian population":"civilian_population.csv",
 "Economically insecure population":"economically_insecure_population.csv",
 "Working age population":"working_age_population.csv",
 "Official poverty (ACS)":"official_poverty_acs.csv",
 "Official poverty (CPS)":"official_poverty_cps.csv",
 "Supplemental poverty":"supplemental_poverty.csv",
 "Price indexes":"price_indexes.csv",
 "Inflation rates":"inflation_rates.csv",
 "Productivity and pay indexes":"productivity_and_pay_indexes.csv",
 "Productivity and pay levels":"productivity_and_pay_levels.csv",
 "Union membership":"union_membership.csv",
 "Historical union membership":"historical_union_membership.csv",
 "Union wage premium":"union_wage_premium.csv",
 "Teacher pay gap":"teacher_pay_gap.csv",
}

names, files, intervals = {}, {}, {}
missing=[]
for eid in union_ids:
    e = coll[eid]
    nm = e["name"]
    names[eid]=nm
    if nm not in name_to_file:
        missing.append((eid,nm))
    else:
        files[eid]=name_to_file[nm]
    intervals[eid]= e["source_metadata"].get("date_intervals") or ["year"]

print("missing filename mapping:", missing)
assert not missing, missing
assert set(files)==set(union_ids)

# write constants.py
with open("src/constants.py","w") as f:
    f.write('"""Static catalog data for the EPI connector — the entity union plus the\n')
    f.write("mapping from indicator id to its display name and its CSV file inside the\n")
    f.write('State of Working America Data Library ZIP. Data, not logic."""\n\n')
    f.write("ENTITY_IDS = [\n")
    for eid in union_ids:
        f.write(f"    {eid!r},\n")
    f.write("]\n\n")
    f.write("# indicator id -> display name (the `indicator` column value inside the CSV)\n")
    f.write("INDICATOR_NAMES = {\n")
    for eid in union_ids:
        f.write(f"    {eid!r}: {names[eid]!r},\n")
    f.write("}\n\n")
    f.write("# indicator id -> CSV filename inside epi_swa_data_library.zip\n")
    f.write("CSV_FILENAMES = {\n")
    for eid in union_ids:
        f.write(f"    {eid!r}: {files[eid]!r},\n")
    f.write("}\n")
print("wrote src/constants.py")

# write per-spec test yamls
os.makedirs("tests", exist_ok=True)
for eid in union_ids:
    sid = f"economic-policy-institute-{eid.lower().replace('_','-')}"
    ivs = intervals[eid]
    lines = [
        f"spec_id: {sid}",
        "status: active",
        "tests:",
        "  - not_null: indicator",
        "  - not_null: data_version",
        "  - not_null: date_interval",
        "  - not_null: year",
        "  - not_null: value",
        f"  - enum: {{col: date_interval, values: [{', '.join(ivs)}]}}",
        "    reason: this indicator publishes only these date intervals per the EPI catalog availability",
        "    certainty: 90",
        "  - row_count: {min: 1}",
        f"  - matches: {{col: data_version, pattern: '^[0-9]{{4}}\\.[0-9]+\\.[0-9]+$'}}",
        "    reason: data_version is the SWA release tag like 2026.6.17",
        "    certainty: 85",
    ]
    with open(f"tests/{sid}.yaml","w") as f:
        f.write("\n".join(lines)+"\n")
print("wrote", len(union_ids), "test yamls")
