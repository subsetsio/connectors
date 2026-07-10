-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Rowid" AS rowid,
    CAST("Year" AS BIGINT) AS year,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "DataSource" AS datasource,
    "Category" AS category,
    "Indicator" AS indicator,
    "Response" AS response,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    CAST("Data_Value" AS DOUBLE) AS data_value,
    CAST("Data_Value_Alt" AS DOUBLE) AS data_value_alt,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    CAST("Low_Confidence_Limit" AS DOUBLE) AS low_confidence_limit,
    CAST("High_Confidence_Limit" AS DOUBLE) AS high_confidence_limit,
    CAST("Number" AS BIGINT) AS number,
    CAST("WeightedNumber" AS BIGINT) AS weightednumber,
    "StratificationCategory1" AS stratificationcategory1,
    "Stratification1" AS stratification1,
    "StratificationCategory2" AS stratificationcategory2,
    "Stratification2" AS stratification2,
    "CategoryID" AS categoryid,
    "IndicatorID" AS indicatorid,
    "Geolocation" AS geolocation,
    CAST("LocationID" AS BIGINT) AS locationid,
    "ResponseID" AS responseid,
    "DataValueTypeID" AS datavaluetypeid,
    "StratificationCategoryID1" AS stratificationcategoryid1,
    "StratificationID1" AS stratificationid1,
    "StratificationCategoryID2" AS stratificationcategoryid2,
    "StratificationID2" AS stratificationid2,
    CAST("value" AS BIGINT) AS value
FROM "cdc-h3my-dzpj"
