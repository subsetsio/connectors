-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Project_Number" AS project_number,
    "Project_Name" AS project_name,
    "Instrument_Type" AS instrument_type,
    "Lending_Instrument" AS lending_instrument,
    "Country" AS country,
    "Country_ISO_code" AS country_iso_code,
    "Department" AS department,
    "Division" AS division,
    CAST("Approval_Year" AS BIGINT) AS approval_year,
    "Approval_Date" AS approval_date,
    "Fund_Currency" AS fund_currency,
    "Original_Approved_Amount" AS original_approved_amount,
    "Use" AS use,
    "Mitigation_Sector" AS mitigation_sector,
    "Adaptation_Sector" AS adaptation_sector,
    "%_Only_Mitigation" AS only_mitigation,
    "%_Only_Adaptation" AS only_adaptation,
    "%_Only_Dual-use" AS only_dual_use,
    "US$_Mitigation" AS us_mitigation,
    "US$_Adaptation" AS us_adaptation,
    "US$_Dual-use" AS us_dual_use,
    "Climate_Finance_Amount" AS climate_finance_amount,
    "source_resource"
FROM "idb-idb-climate-finance-dataset-2024"
