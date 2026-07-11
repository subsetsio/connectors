-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "c0",
    "Equipment" AS equipment,
    "4.2" AS 4_2,
    "4.7" AS 4_7,
    "7.381370826010545" AS 7_381370826010545,
    "Average from" AS average_from,
    "1798",
    "1838",
    "1848",
    "1858",
    "1868",
    "Producers' Durables" AS producers_durables,
    "c1",
    "6",
    "7.7" AS 7_7,
    "13.7" AS 13_7,
    "Kuznets (National Product since 1869, NBER 1946, p. 80) assu" AS kuznets_national_product_since_1869_nber_1946_p_80_assu,
    "c6",
    "c7",
    "Cotton agriculture" AS cotton_agriculture,
    "10",
    "Fogel, Robert W. and Stanley L. Engerman. 1974. Time on the " AS fogel_robert_w_and_stanley_l_engerman_1974_time_on_the
FROM "gpih-property-income-fr-wealth-1850-70"
