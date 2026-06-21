# Station code / name lists for the Hong Kong Observatory Open Data API.
# There is no machine-readable station-catalog endpoint; these are the documented
# station sets from the HKO Open Data API Documentation. Invalid (station,dataType)
# combinations are detected at fetch time via the API's error sentinel and skipped,
# so an over-broad list is safe.

# Daily temperature stations (CLMTEMP / CLMMAXT / CLMMINT share this set).
CLM_STATIONS = [
    "CCH", "CWB", "HKA", "HKO", "HKP", "HKS", "HPV", "JKB", "KLT", "KP",
    "KSC", "KTG", "LFS", "NGP", "PEN", "PLC", "SE1", "SEK", "SHA", "SKG",
    "SKW", "SSH", "SSP", "STY", "TC", "TKL", "TMS", "TPO", "TU1", "TW",
    "TWN", "TY1", "TYW", "VP1", "WGL", "WLP", "WTS", "YCT", "YLP",
]

# Tide stations (HHOT hourly heights / HLT high-low tide times+heights).
TIDE_STATIONS = [
    "CCH", "CLK", "CMW", "KCT", "KLW", "LOP", "MWC", "QUB",
    "SPW", "TAO", "TBT", "TMW", "TPK", "WAG",
]

# RYES (weather & radiation report) station name prefixes used in the flat
# {Station}{Attribute} JSON keys. Longest-prefix matching splits a key into
# (station, attribute); order does not matter (matcher sorts by length).
RYES_STATIONS = [
    "CheungChau", "ChekLapKok", "PingChau", "HKO", "HongKongPark",
    "WongChukHang", "HappyValley", "TseungKwanO", "KatO", "KowloonCity",
    "KingsPark", "KwunTong", "LauFauShan", "TaiMeiTuk", "KaiTakRunwayPark",
    "ShekKong", "ShaTin", "SaiKung", "ShauKeiWan", "ShamShuiPo", "ShaTauKok",
    "Stanley", "SaiWanHo", "TapMun", "TsimBeiTsui", "TaKwuLing", "TaiPo",
    "TuenMun", "TsuenWanShingMunValley", "TsuenWanHoKoon", "TsingYi",
    "WongTaiSin", "YuenLongPark", "YuenNgFan",
]
