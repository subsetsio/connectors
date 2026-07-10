SELECT
    CAST("Factor_Compare" AS VARCHAR) AS "Factor_Compare",
    CAST("Id_Compare" AS VARCHAR) AS "Id_Compare",
    CAST("Language_Compare" AS VARCHAR) AS "Language_Compare",
    CAST("Order_Compare" AS VARCHAR) AS "Order_Compare",
    CAST("Query1_Factor" AS VARCHAR) AS "Query1_Factor",
    CAST("Query1_Id" AS VARCHAR) AS "Query1_Id",
    CAST("Query1_Language" AS VARCHAR) AS "Query1_Language",
    CAST("Query1_Order" AS VARCHAR) AS "Query1_Order",
    CAST("Query1_Signatory" AS VARCHAR) AS "Query1_Signatory",
    CAST("Query2_Factor" AS VARCHAR) AS "Query2_Factor",
    CAST("Query2_Id" AS VARCHAR) AS "Query2_Id",
    CAST("Query2_Language" AS VARCHAR) AS "Query2_Language",
    CAST("Query2_Order" AS VARCHAR) AS "Query2_Order",
    CAST("Query2_Signatory" AS VARCHAR) AS "Query2_Signatory",
    CAST("RowNum" AS VARCHAR) AS "RowNum",
    CAST("Signatory_Compare" AS VARCHAR) AS "Signatory_Compare"
FROM "european-environment-agency-missiononadaptation-signatoryreporting.v-assessment-template-factors-text-comparison"
