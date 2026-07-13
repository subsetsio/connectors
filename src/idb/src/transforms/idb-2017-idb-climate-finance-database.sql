-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Project_Number" AS project_number,
    "Project_Name" AS project_name,
    "Type" AS type,
    "Country" AS country,
    "Department" AS department,
    CAST("Approval_Year" AS BIGINT) AS approval_year,
    "Approval_Date" AS approval_date,
    "Fund_Currency" AS fund_currency,
    CAST("Approved_Amount" AS BIGINT) AS approved_amount,
    "Use" AS use,
    "Mitigation_sector" AS mitigation_sector,
    "Adaptation_sector" AS adaptation_sector,
    CAST("%_Only_mitigation" AS DOUBLE) AS only_mitigation,
    CAST("%_Only_adaptation" AS DOUBLE) AS only_adaptation,
    CAST("%_Only_Dual-use" AS DOUBLE) AS only_dual_use,
    CAST("US$_Mitigation" AS BIGINT) AS us_mitigation,
    CAST("US$_Adaptation" AS BIGINT) AS us_adaptation,
    CAST("US$_Dual-use" AS BIGINT) AS us_dual_use,
    CAST("US$_Total_climate_finance" AS BIGINT) AS us_total_climate_finance,
    "source_resource"
FROM "idb-2017-idb-climate-finance-database"
