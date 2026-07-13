-- provisional pass-through for accepted StatBank table not yet profiled
SELECT
    "papir",
    "kupon",
    "valuta",
    "løbetid" AS l_betid,
    "udstedsektor",
    "udstland",
    "værdian" AS vaerdian,
    "data",
    "time",
    "value"
FROM "danmarks-nationalbank-dnvpu"
