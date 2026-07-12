-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("zipcode" AS BIGINT) AS zipcode,
    CAST("reportingdate" AS TIMESTAMP) AS reportingdate,
    "reasoncc_emp",
    "reasoncc_ed",
    "reasoncc_emped",
    "reasoncc_ps",
    "reasoncc_fedememp",
    "reasoncc_fedemed",
    "reasoncc_fedememped",
    "reasoncc_fedemps",
    CAST("avgfamilysize" AS BIGINT) AS avgfamilysize,
    CAST("avgmonthlyincome" AS BIGINT) AS avgmonthlyincome,
    "singleparent",
    "familyhomeless",
    "familymilitary",
    "primlang_1",
    "primlang_2",
    "primlang_3",
    "primlang_4",
    "primlang_5",
    "primlang_6",
    "primlang_7",
    "primlang_8",
    "primlang_9",
    "primlang_10",
    "primlang_11",
    "primlang_12"
FROM "texas-workforce-commission-socrata-a4gu-yvmu"
