import os, yaml
SLUG="groningen-growth-and-development-centre"
TDIR="tests"; os.makedirs(TDIR, exist_ok=True)

# per entity: list of test dicts
def base(year_lo, year_hi, rows_min, dims, year_certainty=90, year_outward=False):
    t=[{"not_null":d} for d in dims]
    t += [
        {"column_type":{"col":"year","type":"integer"}},
        {"column_type":{"col":"value","type":"float"}},
        {"not_null":"value"},
        {"between":{"col":"year","lo":year_lo,"hi":year_hi},"certainty":year_certainty,
         "reason":"observed year span for this release","points_outward":year_outward,
         "severity":"warn"},
        {"row_count":{"min":rows_min},"reason":"melted long-table size seen while probing"},
    ]
    return t

SPECS={
 "10.34894-fabvlr": base(1950,2025,200000,["countrycode","variable"]),
 "10.34894-qt5bcc": base(1950,2020,200000,["countrycode","variable"]),
 "10.34894-inzbf2": base(1,2025,40000,["countrycode","variable"], year_certainty=70)
   + [{"enum":{"col":"variable","values":["gdppc","pop"]}}],
 "10.34894-aeax1f": base(2000,2025,1000,["countrycode","sector","variable"]),
 "10.34894-lch4ca": base(1990,2025,10000,["country","var","sector"])
   + [{"enum":{"col":"var","values":["VA","EMP"]},"certainty":80,
      "reason":"ETD reports value added and employment","severity":"warn"}],
 "10.34894-e7mvox": base(1990,2025,1000,["country","var","sector"]),
 "10.34894-imkxnt": base(1990,2025,100000,["cnt","tabletype","row_industry","col_industry"])
   + [{"enum":{"col":"tabletype","values":["SUPPLY","USE","IOT"]}}],
 "10.34894-a7axdn": base(1965,2000,100000,["countrycode","var","year"]),
 "10.34894-pj2m1c": base(2000,2014,100000,["country","variable","year"]),
 "10.34894-xdtauz": base(1995,2011,100000,["country","variable","year"]),
 "10.34894-6gdd7q": base(1970,2015,100000,["iso3","var","isic4"]),
}

for eid,tests in SPECS.items():
    spec_id=f"{SLUG}-{eid}"
    doc={"spec_id":spec_id,"status":"active","tests":tests}
    with open(os.path.join(TDIR,spec_id+".yaml"),"w") as f:
        yaml.safe_dump(doc,f,sort_keys=False,allow_unicode=True)
    print("wrote",spec_id+".yaml")
