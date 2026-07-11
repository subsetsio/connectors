-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Span" AS "span",
    "1835-2010" AS "1835_2010",
    "1868-2007" AS "1868_2007",
    "1883-2010" AS "1883_2010",
    "1866-1965" AS "1866_1965",
    "1905-2010" AS "1905_2010",
    "1883-2010_2" AS "1883_2010_2",
    "1882-2010" AS "1882_2010",
    "1917-2005" AS "1917_2005",
    "1879-2010" AS "1879_2010",
    "1840-2010" AS "1840_2010",
    "1825-2009" AS "1825_2009",
    "1900-2010" AS "1900_2010",
    "1909-2005" AS "1909_2005",
    "1906-1983" AS "1906_1983",
    "1850-2010" AS "1850_2010",
    "1789-2010" AS "1789_2010",
    "c0",
    "1867-1996" AS "1867_1996",
    "1867-1998" AS "1867_1998",
    "1920-1997" AS "1920_1997",
    "1918-1994" AS "1918_1994",
    "1867-2010" AS "1867_2010",
    "1884-2010" AS "1884_2010",
    "1759-1965" AS "1759_1965",
    "1883-2000" AS "1883_2000",
    "1898-2010" AS "1898_2010",
    "1925-1993" AS "1925_1993",
    "1925-1993_2" AS "1925_1993_2",
    "1825-2010" AS "1825_2010",
    "1900-2004" AS "1900_2004",
    "1909-2010" AS "1909_2010",
    "1789-1997" AS "1789_1997",
    "1792-1915" AS "1792_1915",
    "1916-1997" AS "1916_1997",
    "1916-2000" AS "1916_2000",
    "1937-1995" AS "1937_1995"
FROM "gpih-ihs-n-america-fiscal-history-20nov"
