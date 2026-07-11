-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "New England" AS "new_england",
    "339.6940609252" AS "339_6940609252",
    "c2",
    "58.52969926563" AS "58_52969926563",
    "35.13734896142" AS "35_13734896142",
    "16.83249179172" AS "16_83249179172",
    "52.191190789240004" AS "52_191190789240004",
    "450.41495098007005" AS "450_41495098007005",
    "New England_2" AS "new_england_2",
    "0.5440586702957" AS "0_5440586702957",
    "2.7279948014600004" AS "2_7279948014600004",
    "165.10843449518734" AS "165_10843449518734",
    "5.014155550498469" AS "5_014155550498469",
    "827.8793732581564" AS "827_8793732581564",
    "c14",
    "c15",
    "WNC" AS "wnc",
    "71.18517713970999" AS "71_18517713970999",
    "2.5443232099999302" AS "2_5443232099999302",
    "13.0433294165" AS "13_0433294165",
    "11.12324768419" AS "11_12324768419",
    "97.89607745039993" AS "97_89607745039993",
    "5.331782148422" AS "5_331782148422",
    "5.791465496933" AS "5_791465496933",
    "11.123247645355" AS "11_123247645355",
    "0.05" AS "0_05",
    "0.073" AS "0_073",
    "106.63564296843998" AS "106_63564296843998",
    "79.33514379360275" AS "79_33514379360275",
    "185.97078676204274" AS "185_97078676204274"
FROM "gpih-regional-hh-incomes-1850-20may14"
