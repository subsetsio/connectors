-- Pass-through for the accepted StatBank DNVPDKR2 table. Grain stays keyless
-- until the fixed large-slice downloader completes and model-verify can prove
-- row identity from the full raw extract.
SELECT
    "typreal",
    "løbetid3" AS l_betid3,
    "løbetid2" AS l_betid2,
    "kupon2",
    "valuta",
    "udsted",
    "invsektor",
    "daekobl",
    "datat",
    "time",
    "value"
FROM "danmarks-nationalbank-dnvpdkr2"
