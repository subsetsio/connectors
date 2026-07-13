-- provisional pass-through for accepted StatBank table not yet profiled
SELECT
    "data",
    "papir",
    "løbetid2" AS l_betid2,
    "invsektor",
    "valuta",
    "time",
    "value"
FROM "danmarks-nationalbank-dnvpsp"
